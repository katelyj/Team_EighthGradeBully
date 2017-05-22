var period = Array(12);
period[0]="Before school|0|28800";
period[1]="Period 1|28800|31260";
period[2]="Period 2|31500|33960";
period[3]="Period 3|34260|36900";
period[4]="Period 4|37200|39660";
period[5]="Period 5|39960|42420";
period[6]="Period 6|42720|45180";
period[7]="Period 7|45480|47940";
period[8]="Period 8|48240|50700";
period[9]="Period 9|50940|53400";
period[10]="Period 10|53640|56100";
period[11]="After school|56100|86340";

var ClientStartTime=0;
var PeriodNames = new Array();
var PeriodStarts = new Array();
var PeriodEnds = new Array();
function Init()
{
	ClientStartTime = ClientSeconds();
	for (var i = 0; i < period.length; ++i)
	{	a=period[i].split('|');
		PeriodNames[i] = a[0];
		PeriodStarts[i] = a[1];
		PeriodEnds[i] = a[2];
	}
	Tick();
}
function Tick()
{	
	document.all['seconds'].innerHTML = DisplaySeconds();
	document.all['hours_minutes'].innerHTML = DisplayHoursMinutes();
	changePeriods();
	setTimeout('Tick()',1000);
}

function ClientSeconds()
{	var d = new Date();
	return d.getHours() * 3600 + d.getMinutes() * 60 + d.getSeconds();	
}
function SecondsNow()
{	var secs = ServerStartTime + ClientSeconds() - ClientStartTime;
	if (secs >= 24*3600)
		secs = secs - 24*3600;
	return secs;
}
function DisplaySeconds()
{	var secs = SecondsNow() % 60;
	if (secs < 10)
		return ':0'+secs;
	else
		return ':'+secs;
}
function DisplayHoursMinutes()
{	var mins = Math.floor(SecondsNow()/60)%60;
	var hours = Math.floor(SecondsNow()/3600);
	if (hours==0)
		hours = 12;
	if (hours > 12)
		hours = hours - 12;
	if (mins < 10){
		console.log(hours+':0'+mins);
		return hours+':0'+mins;
	}
	else{
		console.log(hours+':'+mins);
		return hours+':'+mins;
	}
}
function changePeriods()
{	var pcolors = new Array(period.length);
	var snow = SecondsNow();
	var periodname = '';
	var minutes_into = 0;
	var minutes_left = 0;
	var i;
	var periodid;
	
	for (i = 0; i < period.length; ++i)
		pcolors[i] = 'black';
	
	for (i = 0; i < period.length; ++i)
	{	if (snow >= PeriodStarts[i] && snow <= PeriodEnds[i])
		{	periodname = PeriodNames[i];
			minutes_into = Math.floor((snow-PeriodStarts[i])/60);
			minutes_left = Math.floor((PeriodEnds[i]-PeriodStarts[i])/60) - minutes_into;
			pcolors[i] = 'red';
			break;
		}
		else if (i > 0)
		{	if (snow > PeriodEnds[i-1] && snow < PeriodStarts[i])
			{	periodname='Before ' + PeriodNames[i];
				pcolors[i-1] = 'red';
				pcolors[i] = 'red';
				minutes_into = Math.floor((snow-PeriodEnds[i-1])/60);
				minutes_left = Math.floor((PeriodStarts[i]-PeriodEnds[i-1])/60) - minutes_into;
				break;
			}
		}
	}
	
	if (document.all['PeriodName'].innerHTML != periodname)
		document.all['PeriodName'].innerHTML = periodname;
	if (document.all['minutes_into'].innerHTML != minutes_into)
	{	document.all['minutes_into'].innerHTML = minutes_into;
		document.all['minutes_left'].innerHTML = minutes_left;
	}
	
	for (i = 0; i < period.length; ++i)
	{	periodid='period'+i;
		if (document.all[periodid].style.color != pcolors[i])
			document.all[periodid].style.color = pcolors[i];
	}
}