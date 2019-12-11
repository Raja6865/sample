#!/usr/bin/perl

use CGI;
use DBI;
use LWP::UserAgent;
use HTTP::Request::Common;

print "content-type:text/html\n\n";

my $query = new CGI;

$mobno=$query->param('msisdn');
$keyword=$query->param('keyword');
$shortcode=$query->param('shortcode');

$rkeyword=$keyword;

our $dbuser="root";
our $dbpasswd='kiranku';
our $dsn="DBI:mysql:Hutchcrbt;host=192.168.100.29";
our $dsnb="DBI:mysql:Billing;host=192.168.0.8";
our $dsnd="DBI:mysql:Dialout;host=192.168.0.12";

$mobno=substr($mobno,-9,9);

if($mobno==788323803 || $mobno==789688118 || $mobno==782737445 || $mobno==785001663)
{}
else
{
	exit;
}

if($shortcode=="367")
{}
else
{
	exit;
}


$sid="1";
$subcriptiontype="8";
$subtypename="SMS";

$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
$str=$mysql->prepare("select count(*),lang,activate,subscridate from existnewsubscriber where mobno='$mobno' group by mobno");
$str->execute;
@nesubs=$str->fetchrow();
$str->finish();
$mysql->disconnect();

$necnt=$nesubs[0];
$lang=$nesubs[1];
$activate=$nesubs[2];
$subscridate=$nesubs[3];

if($necnt==0)
{
	$lang=3;
	$userstatus='N';
}
elsif($necnt==1)
{
	if($activate==1) 
	{
		$userstatus='E';
	}
	elsif($activate==2) 
	{
		$lang=3;
		$userstatus='N';
	}
}

$prepos="3";
$agent=LWP::UserAgent->new;
$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
$response=$agent->request($request);
$prepos=$response->content;

if($prepos==0 || $prepos==1)
{}
else
{
	#$message="Server Busy, please try again later.";

	$MsgID="1011";
	&SendConfSMS;

	exit;
}


$keyword=~tr/\$#@~!&*"'%\-_=+()[]{}<>;.,:?^`\|\\\///d;
$keyword=~s/space/ /gi;

$GTChars=substr($keyword,0,2);

if(uc($GTChars) eq "GT")
{
	$fword=substr($keyword,0,2);
	$sword=substr($keyword,2);

	$keyword="$fword "."$sword";
}

$keyword = join(' ',split(' ',$keyword));

@array=split(' ',$keyword);
$argcnt=@array;

$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
$mysql->do("insert into SMSKeywordsLogs (mobno,lang,date,rkeyword,keyword,shortcode,subcriptiontype,subtypename,userstatus,serverid,prepos) values ('$mobno','$lang',now(),'$rkeyword','$keyword','$shortcode','$subcriptiontype','$subtypename','$userstatus','$sid','$prepos')");
$mysql->disconnect();


if(uc($array[0]) eq "HT")
{
	if(uc($array[1]) eq "DA")
	{
		if($argcnt==2)
		{
			&HTDA;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	elsif(uc($array[1]) eq "Y")
	{		
		if($argcnt==2)
		{
			&HTY;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	elsif(uc($array[1]) eq "N")
	{
		if($argcnt==2)
		{
			&HTN;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	elsif($array[1] =~ (/^\d+\z/))
	{
		if(length($array[1])==6)
		{
			$tuneid=$array[1];

			&HTTUNEID;
		}
		elsif(length($array[1])!=6)
		{
			#$message="The tune ID you sent is incorrect. Please send with the correct Tune ID.";

			$MsgID="1005";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Please send the proper keyword.";

		$MsgID="1037";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "GET")
{
	if($array[1] =~ (/^\d+\z/))
	{
		if(length($array[1])==6)
		{
			$tuneid=$array[1];

			&GETTUNEID;
		}
		elsif(length($array[1])!=6)
		{
			#$message="The tune ID you sent is incorrect. Please send with the correct Tune ID.";

			$MsgID="1017";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Please send the proper keyword.";

		$MsgID="1037";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "GIFT")
{
	if(uc($array[1]) eq "DA")
	{
		if($array[2] =~ (/^\d+\z/))
		{
			$assignto=$array[2];

			&GIFTDA;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Please send the proper keyword.";

		$MsgID="1037";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "BT")
{
	if($array[1] eq "")
	{
		#$message="Send BT<space>(Tune Name)<space>(Language)<space>(Duration) to 369. E.g. BT MEETING S 3 to activate MEETING Busy Tune in Sinhala for 3 Hours. Tune Names: BUSY,DRIVING,MEETING,UNWELL,CLASS,MOVIE,WORK,HOLIDAY,SLEEPING,GYM,LUNCH,NO PHONE,RAIN,PLAYING,DINNER,DOCTOR,BATTERY,TRAINING,VISITORS,ROAMING";

		$MsgID="1043";
		&SendConfSMS;

		exit;
	}
	elsif(uc($array[1]) eq "DA")
	{
		if($argcnt==2)
		{
			&BTDA;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	elsif(uc($array[1]) eq "SUB")
	{
		if($argcnt==2)
		{
			&BTSUB;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		$i=1;$message='';
		while($i<$argcnt)
		{
			$message="$message"."$array[$i] ";
			$i++;
		}

		chop($message);

		&BTMESSAGE;
	}
}
elsif(uc($array[0]) eq "CT")
{
	if(uc($array[1]) eq "DA")
	{
		if($argcnt==2)
		{
			&CTDA;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="The keyword sent is incorrect. To deactivate type HT DA for Hello tunes, BT DA for Busy tunes, CT DA for copy tunes, UNSUB UT for Unlimited tunes.";

		$MsgID="1042";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "HELP")
{
	if($array[1] eq "")
	{
		#$message="Tune activations send HT <Tune ID> to 369,add tune to Juke Box: GET <Tune ID>, Deactivation: HT DA, Deactivate Copy Tune: CT DA, Deactivate Gift Tune: GIFT DA <GIFTMOBNO>, Deactivate Busy Tune: BT DA";

		$HELP="1";
		$MsgID="1072";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "NT")
{
	if(uc($array[1]) eq "DA")
	{
		if($argcnt==2)
		{
			&NTDA;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		$i=1;$message='';
		while($i<$argcnt)
		{
			$message="$message"."$array[$i] ";
			$i++;
		}

		chop($message);
		$name=$message;

		&NTNAME;
	}
}
elsif(uc($array[0]) eq "NTOPT")
{
	if($array[1] =~ (/^\d+\z/))
	{
		$reply=$array[1];
		&NTOPT;
	}
	else
	{
		#$message="Please send the proper keyword.";

		$MsgID="1037";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "SUB")
{
	if(uc($array[1]) eq "UT")
	{
		if($argcnt==2)
		{
			&SUBUT;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Please send the proper keyword.";

		$MsgID="1037";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "UNSUB")
{
	if(uc($array[1]) eq "UT")
	{
		if($argcnt==2)
		{
			&UNSUBUT;
		}
		else
		{
			#$message="Please send the proper keyword.";

			$MsgID="1037";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="The keyword sent is incorrect. To deactivate type HT DA for Hello tunes, BT DA for Busy tunes, CT DA for copy tunes, UNSUB UT for Unlimited tunes.";

		$MsgID="1042";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "HTDA" || uc($array[0]) eq "HTD")
{
	if($argcnt==1)
	{
		&HTDA;
	}
	else
	{
		#$message="Please send the proper keyword.";

		$MsgID="1037";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "UNSUBUT")
{
	if($argcnt==1)
	{
		&UNSUBUT;
	}
	else
	{
		#$message="Please send the proper keyword.";

		$MsgID="1037";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "BTDA" || uc($array[0]) eq "BTD")
{
	if($argcnt==1)
	{
		&BTDA;
	}
	else
	{
		#$message="Please send the proper keyword.";

		$MsgID="1037";
		&SendConfSMS;

		exit;
	}
}
elsif(uc($array[0]) eq "GT")
{
=pod
	if($mobno==788323803 || $mobno==789688118 || $mobno==782737445 || $mobno==785001663)
	{}
	else
	{
		exit;
	}
=cut

	$i=1;$songname='';
	while($i<$argcnt)
	{
		$songname="$songname"."$array[$i] ";
		$i++;
	}

	chop($songname);

	&GTSONGNAME;
}
else
{
	#$message="Please send the proper keyword.";

	$MsgID="1037";
	&SendConfSMS;

	exit;
}


sub HTTUNEID
{
	$sid="1";
	$subcriptiontype="8";
	$subtypename="SMS";
	$freetune="0";
	$promoid="0";
	$fbillamt="0";
	$balance="0";
	$RenewalFlag="0";
	$ARBflag="0";

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),lang,activate,subscridate from existnewsubscriber where mobno='$mobno' group by mobno");
	$str->execute;
	@nesubs=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$necnt=$nesubs[0];
	$lang=$nesubs[1];
	$activate=$nesubs[2];
	$subscridate=$nesubs[3];

	if($necnt==0)
	{
		$lang=3;
		$userstatus='N';
	}
	elsif($necnt==1)
	{
		if($activate==1) 
		{
			$userstatus='E';
		}
		elsif($activate==2) 
		{
			$lang=3;
			$userstatus='N';
		}
	}

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1011";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to activate the requested Hello Tune since you are Pre activated with a Corporate tune. When this expires U will be enabled for normal activation.";

		$MsgID="1009";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################
        
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select tunenumber,tunetype,concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tuneid='$tuneid' and ivrno<>0 and IsValid=1");
	$str->execute;
	@tunearr=$str->fetchrow();
	$tunecnt=$str->rows;
	$str->finish();
	$mysql->disconnect();

	$tunenumber=$tunearr[0];
	$tunetype=$tunearr[1];
	$MTRcomment=$tunearr[2];

	if($tunecnt==0)
	{
		#$message="The tune ID you sent is incorrect. Please send with the correct Tune ID.";

		$MsgID="1005";
		&SendConfSMS;

		exit;
	}
	elsif($tunecnt>0)
	{
		########################################### Checking for Existance of Same Tune ########################################### 

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$str=$mysql->prepare("select count(*) from subscriber where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1");
		$str->execute;
		$subscnt=$str->fetchrow();
		$str->finish();

		$str=$mysql->prepare("select count(*) from jukebox where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1");
		$str->execute;
		$jukecnt=$str->fetchrow();
		$str->finish();

		$mysql->disconnect();

		if($subscnt==0 && $jukecnt==0)
		{}
		elsif($subscnt==1 || $jukecnt==1)
		{
			#$message="Dear Customer, you are already activated with the requested tune. Please try again with another tune. Thank you.";

			$MsgID="1006";
			&SendConfSMS;

			exit;
		}

		########################################### Checking for Existance of Same Tune ########################################### 

		#################################### Charges and Expdates Calculation -- Start ######################################

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$str=$mysql->prepare("select preamt,postamt,tax from charges");
		$str->execute;
		@charges=$str->fetchrow();
		$str->finish();

		$preamt=$charges[0];
		$postamt=$charges[1];
		$tax=$charges[2];

		$tax=($tax/100);

		$str=$mysql->prepare("select (CASE 1 WHEN DAY(curdate())<18 THEN DATE_FORMAT(curdate(),'%Y-%m-18') WHEN DAY(curdate())>=18 THEN DATE_FORMAT(curdate() + INTERVAL 1 MONTH,'%Y-%m-18') ELSE '' END) as ExpDate,(select round((('$postamt'/30) * '$tax' + ('$postamt'/30))*(CASE 1 WHEN DAY(curdate())<18 THEN DATEDIFF(DATE_FORMAT(curdate(),'%Y-%m-18'),curdate()) WHEN DAY(curdate())>=18 THEN DATEDIFF(DATE_FORMAT(curdate() + INTERVAL 1 MONTH,'%Y-%m-18'),curdate()) ELSE '' END),2))");
		$str->execute;
		@postpaid=$str->fetchrow();
		$str->finish();

		$postexpdate=$postpaid[0];
		$postamount=$postpaid[1];

		$str=$mysql->prepare("select curdate() + INTERVAL 30 DAY,curdate() + INTERVAL 90 DAY,round((($preamt/30) * $tax + ($preamt/30))*30,2)");
		$str->execute;
		@prnpr=$str->fetchrow();
		$str->finish();

		$prexpdate=$prnpr[0];
		$nprexpdate=$prnpr[1];
		$prnpramt=$prnpr[2];

		$mysql->disconnect();

		##################################### Charges and Expdates Calculation -- End #######################################

		if($prepos==1)
		{
			$expdate=$postexpdate;
			$amount=$postamount;
		}
		elsif($prepos==0)
		{
			if(substr($tunetype,0,2) eq "PR")
			{
				$expdate=$prexpdate;
				$amount=$prnpramt;
			}
			elsif(substr($tunetype,0,2) eq "NP")
			{
				$expdate=$nprexpdate;
				$amount=$prnpramt;
			}

			&MicroCharging;
		}

		if($skipbilling==1)
		{
			$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
			$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,status,fbillamt,balance,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',1,'$retval','$fbillamt','$balance','$amount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$prepos')");
			$bsql->disconnect();

			$skipbilling=0;
		}
		else
		{
			$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
			$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,fbillamt,balance,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',1,'$fbillamt','$balance','$amount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$prepos')");
			$bsql->disconnect();

			$agent=LWP::UserAgent->new;
			$request=POST "http://192.168.100.28/inbilling/WebForm1.aspx?msisdn=$mobno&amount=$amount&tunetype=$tunetype&tunenumber=$tunenumber&billsrc=2&CP=$MTRcomment&subtype=$subcriptiontype&subtypename=$subtypename";
			$response=$agent->request($request);
			$rep=$response->as_string;
			@extract=split('\\n',$rep);
			$retval=$extract[$#extract];

			$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
			$bsql->do("update billing set date=now(),status='$retval' where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and status=0 and date(date)=curdate() and amount='$amount' order by date desc limit 1");
			$bsql->disconnect();
		}

		if($necnt==0)
		{
			$subscridate=`date "+%F %T"`;
			chomp($subscridate);
		}
		elsif($necnt==1)
		{
			if($userstatus eq "N")
			{
				$subscridate=`date "+%F %T"`;
				chomp($subscridate);
			}
		}

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$mysql->do("insert into existnewsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,fbillamt,balance,amount,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$expdate',1,'$subscridate','$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$fbillamt','$balance','$amount',1,'$MTRcomment','$freetune','$promoid','$prepos')");
		$mysql->disconnect();

		if($retval==1)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			if($necnt==0)
			{
				$mysql->do("insert into existnewsubscriber (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$expdate',1,now(),'$subcriptiontype','$subtypename','$sid','$userstatus','$retval',1,'$MTRcomment','$freetune','$promoid','$prepos')");
			}
			elsif($necnt==1)
			{
				if($userstatus eq "N")
				{
					$mysql->do("update existnewsubscriber set assignto=0,lang='$lang',tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',activate=1,subscridate=now(),subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',billed='$retval',HTservice=1,MTRcomment='$MTRcomment',freetune='$freetune',promoid='$promoid',prepos='$prepos'  where mobno='$mobno'");
				}
				elsif($userstatus eq "E")
				{
					$mysql->do("update existnewsubscriber set assignto=0,lang='$lang',tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',activate=1,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',billed='$retval',HTservice=1,MTRcomment='$MTRcomment',freetune='$freetune',promoid='$promoid',prepos='$prepos' where mobno='$mobno'");
				}
			}

			$str=$mysql->prepare("select count(*),JKflag from subscriber where mobno='$mobno' group by mobno");
			$str->execute;
			@subs=$str->fetchrow();
			$str->finish();

			$subscnt=$subs[0];
			$JKflag=$subs[1];

			$mysql->disconnect();

			if($subscnt==0)
			{
				$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

				$mysql->do("insert into subscriber (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,'$userstatus','$subcriptiontype','$subtypename','$sid','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");
				$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,billed,amount,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,'$userstatus','$subcriptiontype','$subtypename','$sid','$retval','$amount','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");

				$mysql->disconnect();
			}
			elsif($subscnt==1)
			{
				$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

				$mysql->do("update subscriber set tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',sdate=now(),playdate='$expdate',activate=1,userstatus='$userstatus',subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',RenewalFlag='$RenewalFlag',freetune='$freetune',promoid='$promoid',prepos='$prepos',ARBflag='$ARBflag' where mobno='$mobno'");

				$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,billed,amount,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,0,'$userstatus','$subcriptiontype','$subtypename','$sid','$retval','$amount','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");

				$mysql->disconnect();

				if($JKflag==1)
				{
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$str=$mysql->prepare("select sno,TuneSN from jukebox where activate=1 and deftune=1 and mobno='$mobno'");
					$str->execute;
					@juke=$str->fetchrow();
					$str->finish();

					$sno=$juke[0];
					$deftunesn=$juke[1];

					$mysql->do("update jukebox set tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',sdate=now(),playdate='$expdate',activate=1,userstatus='$userstatus',subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',RenewalFlag='$RenewalFlag',freetune='$freetune',promoid='$promoid',prepos='$prepos',ARBflag='$ARBflag' where sno='$sno'");

					$mysql->do("insert into jukeboxmis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid,billed,amount,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,'$deftunesn','$userstatus','$subcriptiontype','$subtypename','$sid','$retval','$amount','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");

					$mysql->disconnect();
				}
			}

			if($microsms==1)
			{
				$microsms="0";
				#$message="You will be charged with Rs.$billeddays %2B Tax %26 a daily fee of Rs.1.50. The tune is valid for $nobdays days.";

				$MsgID="1004";
				&SendConfSMS;

				exit;
			}
			else
			{
				$Response=substr($tunetype,0,2);

				if($Response eq "PR")
				{
					if($prepos==0)
					{
						#$message="Thank you for using Premium Tunes. You will be charged a tune subscription of Rs.30 %2B Tax %26 a daily fee of Rs.1.50. The tune is valid for 30 days.";

						$MsgID="1000";
					}
					elsif($prepos==1)
					{
						#$message="Thank you for using Hello Tunes. You will be charged a tune subscription of Rs.40 %2B Tax. The tune is valid for 30 days.";

						$MsgID="1001";
					}
				}
				elsif($Response eq "NP")
				{
					if($prepos==0)
					{
						#$message="Thank you for using Non Premium Tunes. You will be charged a tune subscription of Rs.30 %2B Tax %26 a daily fee of Rs.1.50. The tune is valid for 90 days.";

						$MsgID="1002";
					}
					elsif($prepos==1)
					{
						#$message="Thank you for using Hello Tunes. U will be charged with a tune subscription of Rs.40 %2B Tax. The tune is valid for 30 days.";

						$MsgID="1003";
					}
				}

				&SendConfSMS;

				exit;
			}
		}
		elsif($retval==4)
		{
			#$message="Your tune request has failed due to low balance. Recharge your account and try again. Thank you.";

			$MsgID="1007";
			&SendConfSMS;

			exit;
		}
		else
		{
			#$message="Your tune request has failed. Please try again later. Thank you.";

			$MsgID="1008";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1011";
		&SendConfSMS;

		exit;
	}
}


sub MicroCharging
{
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

	$fbillamt=$amount;

	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/CheckBalance/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$Orignalbalance=$response->content;
	
	if($mobno==789688118 || $mobno==782737445 || $mobno==788323803)
	{
		$Orignalbalance=20;
	}

	$balance=$Orignalbalance;

	if(substr($tunetype,0,2) eq "PR" || substr($tunetype,0,2) eq "NP")
	{
		if($balance >= $fbillamt)
		{
			if(substr($tunetype,0,2) eq "PR")
			{
				$expdate=$prexpdate;
				$amount=$prnpramt;
			}
			elsif(substr($tunetype,0,2) eq "NP")
			{
				$expdate=$nprexpdate;
				$amount=$prnpramt;
			}
		}
		elsif($balance < $fbillamt)
		{
			$minbalance="5";

			$balance=$Orignalbalance - $minbalance;

			$billamt=$balance;

			$str=$mysql->prepare("select min(amount) from microcharges");
			$str->execute;
			$minbillamt=$str->fetchrow();
			$str->finish();

			if($billamt>=$minbillamt)
			{
				$microsms="1";

				$str=$mysql->prepare("select prdays,nprdays,amount from microcharges where amount<='$billamt' order by amount desc limit 1");
				$str->execute;
				@microcharges=$str->fetchrow();
				$str->finish();

				$prdays=$microcharges[0];
				$nprdays=$microcharges[1];
				$amount=$microcharges[2];

				$billeddays=$prdays;

				if(substr($tunetype,0,2) eq "PR")
				{
					$expdays=$prdays;
					$nobdays=$prdays;
				}
				elsif(substr($tunetype,0,2) eq "NP")
				{
					$expdays=$nprdays;
					$nobdays=$nprdays;
				}

				$str=$mysql->prepare("select curdate() + INTERVAL '$expdays' DAY");
				$str->execute;
				$expdate=$str->fetchrow();
				$str->finish();
			}
			else
			{
				$retval="4";
				$skipbilling="1";
				$amount="0";
				$expdays="0";

				$str=$mysql->prepare("select curdate() + INTERVAL '$expdays' DAY");
				$str->execute;
				$expdate=$str->fetchrow();
				$str->finish();
			}
		}
	}

	$mysql->disconnect();
}



sub HTDA
{
	$sid=1;
	$subcriptiontype="8";
	$subtypename="SMS";

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),HTservice,userstatus,lang from existnewsubscriber where mobno='$mobno' group by mobno");
	$str->execute;
	@arr=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$nesubscnt=$arr[0];
	$HTservice=$arr[1];
	$userstatus=$arr[2];
	$lang=$arr[3];

	if($nesubscnt==0)
	{
		#$message="You are not a subscriber of HelloTunes. To Activate the Service please call 369. Charges Apply.";

                $lang="3";
                $userstatus='N';

		$MsgID="1026";
		&SendConfSMS;

		exit;
	}
	elsif($nesubscnt==1)
	{
		if($HTservice==1)
		{
			################################################# CHECK CORPORATE TUNE #################################################

			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
			$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
			$str->execute;
			$Corpcount=$str->fetchrow();
			$str->finish();
			$mysql->disconnect();

			if($Corpcount==1)
			{
				#$message="We are unable to deactivate your helloTune service, since you are Pre activated with Corporate tune.Thank you. Hutch";

				$MsgID="1030";
				&SendConfSMS;

				exit;
			}

			################################################# CHECK CORPORATE TUNE #################################################

			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			$str=$mysql->prepare("select count(*) from subscriber where mobno='$mobno' and activate=1 and (freetune in (1,2) OR promoid=388)");
			$str->execute;
			$freesubscnt=$str->fetchrow();
			$str->finish();

			$str=$mysql->prepare("select count(*) from jukebox where mobno='$mobno' and activate=1 and (freetune in (1,2) OR promoid=388)");
			$str->execute;
			$freejukecnt=$str->fetchrow();
			$str->finish();


			$mysql->disconnect();

			if($freesubscnt==1 || $freejukecnt==1)
			{
				&CheckFreeTune;
				exit;
			}

			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			$str=$mysql->prepare("select assignto,tunenumber,tunetype,date,expdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,prepos from gift where activate=1 and mobno='$mobno' order by date desc limit 1");
			$str->execute;
			@gifttune=$str->fetchrow();
			$gtrows=$str->rows;
			$str->finish();

			$gtassignto=$gifttune[0];
			$gttunenumber=$gifttune[1];
			$gttunetype=$gifttune[2];
			$gtdate=$gifttune[3];
			$gtexpdate=$gifttune[4];
			$gtactivate=$gifttune[5];
			$gtuserstatus=$gifttune[6];
			$gtsubtype=$gifttune[7];
			$gtsubtypename=$gifttune[8];
			$gtserverid=$gifttune[9];
			$gtRenewalFlag=$gifttune[10];
			$gtprepos=$gifttune[11];

			if($gtrows==0)
			{
				$mysql->do("update existnewsubscriber set date=now(),activate=2,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',HTservice=2 where mobno='$mobno'");
				$mysql->do("insert into existnewsubscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid,HTservice,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid',2,'$prepos')");
			}
			elsif($gtrows>0)
			{
				$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunetype='$gttunetype' and tunenumber='$gttunenumber'");
				$str->execute;
				$MTRcomment=$str->fetchrow();
				$tunecnt=$str->rows;
				$str->finish();

				$MTRcomment="$MTRcomment : GIFT $gtassignto";

				$mysql->do("update existnewsubscriber set assignto='$gtassignto',tunenumber='$gttunenumber',tunetype='$gttunetype',date='$gtdate',expdate='$gtexpdate',activate='$gtactivate',subcriptiontype='$gtsubtype',subtypename='$gtsubtypename',serverid='$gtserverid',userstatus='$gtuserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',freetune=0,promoid=0,prepos='$gtprepos' where mobno='$mobno'");
				$mysql->do("insert into existnewsubscribermis (mobno,assignto,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,prepos) values ('$mobno','$gtassignto','$gttunenumber','$gttunetype','$gtdate','$gtexpdate','$gtactivate','$gtsubtype','$gtsubtypename','$gtserverid','$gtuserstatus',1,2,'$MTRcomment','$gtprepos')");
			}

			$mysql->do("insert into deactivated (mobno,lang,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno','$lang',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

			$mysql->do("delete from subscriber where mobno='$mobno'");
			$mysql->do("insert into subscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

			$mysql->do("delete from jukebox where mobno='$mobno'");
			$mysql->do("insert into jukeboxmis(mobno,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

			$mysql->do("delete from sptime where mobno='$mobno'");
			$mysql->do("insert into sptimemis(mobno,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

			$mysql->do("delete from spcaller where mobno='$mobno'");
			$mysql->do("insert into spcallermis(mobno,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

			$mysql->do("delete from spgroup where mobno='$mobno'");
			$mysql->do("insert into spgroupmis(mobno,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

			$mysql->do("delete from tunepack where mobno='$mobno'");
			$mysql->do("insert into tunepackmis (mobno,date,activate,subcriptiontype,subtypename,serverid,prepos)  values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

			$mysql->disconnect();

			#$message="You have successfully deactivated your hello tune service. Thank you for using Hutch.";

			$userstatus='E';

			$MsgID="1027";
			&SendConfSMS;

			exit;
		}
		elsif($HTservice==2)
		{
			#$message="You are Already Deactivated, To Activate the Service please call 369. Charges Apply.";

			$userstatus='E';

			$MsgID="1028";
			&SendConfSMS;

			exit;
		}
	}
	else 
	{
		#$message="Server Busy, please try later.";

		$userstatus='E';

		$MsgID="1031";
		&SendConfSMS;

		exit;
	}
}


sub CheckFreeTune
{
	$flag=0;
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

	$str=$mysql->prepare("select count(*) from subscriber where mobno='$mobno' and activate=1 and (freetune in (1,2) OR promoid=388)");
	$str->execute;
	$subscnt=$str->fetchrow();
	$str->finish();

	$str=$mysql->prepare("select count(*) from jukebox where mobno='$mobno' and activate=1");
	$str->execute;
	$jukecnt=$str->fetchrow();
	$str->finish();

	$str=$mysql->prepare("select count(*),sno,tunenumber,tunetype,deftune,TuneSN,prepos from jukebox where mobno='$mobno' and activate=1 and (freetune in (1,2) OR promoid=388)");
	$str->execute();
	@arr=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$jukefreecnt=$arr[0];
	$sno=$arr[1];
	$juketuneno=$arr[2];
	$juketunety=$arr[3];
	$deftune=$arr[4];
	$TuneSN=$arr[5];
	$jprepos=$arr[6];

	if($subscnt==1 || $jukefreecnt==1)
	{
		if($jukecnt==0)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			$mysql->do("delete from subscriber where mobno='$mobno'");
			$mysql->do("insert into subscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");
			$mysql->do("update NONUSERIVRPromotion set date=now(),activate=2,topick=2 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");

			$mysql->do("update NONUSEROBDIBDpromotion set date=now(),activate=2 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");
			$mysql->disconnect();

                        $mysqld = DBI->connect($dsnd,$dbuser,$dbpasswd);
                        $mysqld->do("update MANSMSOBDpromobase_20Jan2015 set activate=2,date=now(),topick=4 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");
                        $mysqld->disconnect();
			
			#$message="Ur FREE TUNE is now deactivated. If U wish to deactivate other tunes please send HT DA to 369.";
			$userstatus='E';

			$MsgID="1029";
			&SendConfSMS;
		}
		if($jukecnt==1)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			$mysql->do("delete from subscriber where mobno='$mobno'");
			$mysql->do("insert into subscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

			$mysql->do("delete from jukebox where mobno='$mobno'");
			$mysql->do("insert into jukeboxmis(mobno,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

			$mysql->do("update NONUSERIVRPromotion set date=now(),activate=2,topick=2 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");

			
			$mysql->do("update NONUSEROBDIBDpromotion set date=now(),activate=2 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");

			$mysql->disconnect();

                        $mysqld = DBI->connect($dsnd,$dbuser,$dbpasswd);
                        $mysqld->do("update MANSMSOBDpromobase_20Jan2015 set activate=2,date=now(),topick=4 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");
                        $mysqld->disconnect();

			#$message="Ur FREE TUNE is now deactivated. If U wish to deactivate other tunes please send HT DA to 369.";

			$userstatus='E';

			$MsgID="1029";
			&SendConfSMS;
		}

		if($jukefreecnt==1 && $jukecnt==2)
		{        
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			$str=$mysql->prepare("select tunenumber,tunetype,date,expdate,sdate,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag from jukebox where mobno='$mobno' and activate=1 and freetune<>2 and promoid<>388");
			$str->execute();
			@arr=$str->fetchrow();
			$str->finish();

			$jtunenumber=$arr[0];
			$jtunetype=$arr[1];
			$jdate=$arr[2];
			$jexpdate=$arr[3];
			$jsdate=$arr[4];
			$jpalydate=$arr[5];
			$jactivate=$arr[6];
			$juserstatus=$arr[7];
			$jsubcriptiontype=$arr[8];
			$jsubtypename=$arr[9];
			$jserverid=$arr[10];
			$jRenewalFlag=$arr[11];
			$jfreetune=$arr[12];
			$jpromoid=$arr[13];
			$jprepos=$arr[14];
			$jARBflag=$arr[15];

			$mysql->do("update subscriber set tunenumber='$jtunenumber',tunetype='$jtunetype',date='$jdate',expdate='$jexpdate',sdate='$jsdate',playdate='$jpalydate',activate='$jactivate',JKflag=0,userstatus='$juserstatus',subcriptiontype='$jsubcriptiontype',subtypename='$jsubtypename',serverid='$jserverid',RenewalFlag='$jRenewalFlag',freetune='$jfreetune',promoid='$jpromoid',prepos='$jprepos',ARBflag='$jARBflag' where mobno='$mobno'");
			$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$jtunenumber','$jtunetype','$jdate','$jexpdate','$jsdate','$jplaydate','$jactivate',1,'$juserstatus','$jsubcriptiontype','$jsubtypename','$jserverid','$jRenewalFlag','$jfreetune','$jpromoid','$jprepos','$jARBflag')");

			$mysql->do("delete from jukebox where mobno='$mobno'");
			$mysql->do("insert into jukeboxmis(mobno,tunenumber,tunetype,date,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid) values ('$mobno','$juketuneno','$juketunety',now(),2,'$TuneSN','$userstatus','$subcriptiontype','$subtypename','$sid')");

			$mysql->do("update NONUSERIVRPromotion set date=now(),activate=2,topick=2 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");

			$mysql->do("update NONUSEROBDIBDpromotion set date=now(),activate=2 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");

			$mysql->disconnect();

                        $mysqld = DBI->connect($dsnd,$dbuser,$dbpasswd);
                        $mysqld->do("update MANSMSOBDpromobase_20Jan2015 set activate=2,date=now(),topick=4 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");
                        $mysqld->disconnect();

			#$message="Ur FREE TUNE is now deactivated free of charge. If U wish to deactivate other tunes please send HT DA to 369.";

			$userstatus='E';

			$MsgID="1029";
			&SendConfSMS;

			exit;
		}
		elsif($jukecnt>=2)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			if($deftune==0)
			{
				$mysql->do("delete from jukebox where sno='$sno'");
			}
			elsif($deftune==1)
			{
				$mysql->do("delete from jukebox where sno='$sno'");

				$str=$mysql->prepare("select sno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag from jukebox where mobno='$mobno' order by date desc limit 1");
				$str->execute;
				@juketunes=$str->fetchrow();
				$str->finish();

				$jksno=$juketunes[0];
				$jktuneno=$juketunes[1];
				$jktunety=$juketunes[2];
				$jkdate=$juketunes[3];
				$jkexpdate=$juketunes[4];
				$jksdate=$juketunes[5];
				$jkplaydate=$juketunes[6];
				$jkactivate=$juketunes[7];
				$jkuserstatus=$juketunes[8];
				$jksubtype=$juketunes[9];
				$jksubtyname=$juketunes[10];
				$jksid=$juketunes[11];
				$jkRenewalFlag=$juketunes[12];
				$jkfreetune=$juketunes[13];
				$jkpromoid=$juketunes[14];
				$jkprepos=$juketunes[15];
				$jkARBflag=$juketunes[16];

				$mysql->do("update jukebox set deftune=0 where mobno='$mobno'");
				$mysql->do("update jukebox set deftune=1 where sno='$jksno'");

				$mysql->do("update subscriber set tunenumber='$jktuneno',tunetype='$jktunety',date='$jkdate',expdate='$jkexpdate',sdate='$jksdate',playdate='$jkplaydate',activate='$jkactivate',userstatus='$jkuserstatus',subcriptiontype='$jksubtype',subtypename='$jksubtyname',serverid='$jksid',RenewalFlag='$jkRenewalFlag',freetune='$jkfreetune',promoid='$jkpromoid',prepos='$jkprepos',ARBflag='$jkARBflag' where mobno='$mobno'");
				$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$jktuneno','$jktunety','$jkdate','$jkexpdate','$jksdate','$jkplaydate','$jkactivate',1,'$jkuserstatus','$jksubtype','$jksubtyname','$jksid','$jkRenewalFlag','$jkfreetune','$jkpromoid','$jkprepos','$jkARBflag')");

				$mysql->disconnect();
			}

			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
			$maxsno=$maxsno-1;
			$mysql->do("update jukebox set TuneSN=TuneSN-1 where TuneSN>'$TuneSN' and mobno='$mobno'");
			$mysql->do("insert into jukeboxmis(mobno,tunenumber,tunetype,date,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid,prepos) values ('$mobno','$juketuneno','$juketunety',now(),2,'$TuneSN','$jkuserstatus','$subcriptiontype','$subtypename','$jksid','$jkprepos')");

			$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunenumber='$jktuneno' and tunetype='$jktunety'");
			$str->execute;
			$MTRcomment=$str->fetchrow();
			$str->finish();
		

			$mysql->do("update existnewsubscriber set assignto=0,tunenumber='$jktuneno',tunetype='$jktunety',date='$jkdate',expdate='$jkexpdate',activate='$jkactivate',subcriptiontype='$jksubtype',subtypename='$jksubtyname',serverid='$jksid',userstatus='$jkuserstatus',billed=1,HTservice=1,MTRcomment='$MTRcomment',freetune=0,promoid=0,prepos='$jkprepos' where mobno='$mobno'");
			$mysql->do("insert into existnewsubscribermis (mobno,assignto,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,prepos) values ('$mobno',0,'$jktuneno','$jktunety','$jkdate','$jkexpdate','$jkactivate','$jksubtype','$jksubtyname','$jksid','$jkuserstatus',1,1,'$MTRcomment','$jkprepos')");

			$mysql->do("insert into deactivated (mobno,lang,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno','$lang',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");
			$mysql->do("update NONUSERIVRPromotion set date=now(),activate=2,topick=2 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");

			$mysql->do("update NONUSEROBDIBDpromotion set date=now(),activate=2 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");

			$mysql->disconnect();

                        $mysqld = DBI->connect($dsnd,$dbuser,$dbpasswd);
                        $mysqld->do("update MANSMSOBDpromobase_20Jan2015 set activate=2,date=now(),topick=4 where mobno='$mobno' and DATEDIFF(curdate(),date(insdate)) in (0,1,2,3,4) and activate=1");
                        $mysqld->disconnect();

			#$message="Ur FREE TUNE is now deactivated. If U wish to deactivate other tunes please send HT DA to 369.";

			$userstatus='E';

			$MsgID="1029";
			&SendConfSMS;

			exit;
		}
######################################### Finding Active tunes from ALL features #########################################

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		@features=(spgroup,spcaller,sptime,tunepack,gift);
		foreach $table (@features)
		{
			$flag=0;
			if($table eq "spgroup")
			{
				$str=$mysql->prepare("select assignto,groupnumber,tunenumber,tunetype,date,expdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,prepos from spgroup where mobno='$mobno' and mobno=assignto and groupnumber>0 and playdate + INTERVAL 7 DAY > curdate() and activate=1 order by date desc limit 1");
				$str->execute;
				@spgroup=$str->fetchrow();
				$spgrows=$str->rows;
				$str->finish();

				$spgassignto=$spgroup[0];
				$spggrpnumber=$spgroup[1];
				$spgtunenumber=$spgroup[2];
				$spgtunetype=$spgroup[3];
				$spgdate=$spgroup[4];
				$spgexpdate=$spgroup[5];
				$spgactivate=$spgroup[6];
				$spguserstatus=$spgroup[7];
				$spgsubtype=$spgroup[8];
				$spgsubtypename=$spgroup[9];
				$spgserverid=$spgroup[10];
				$spgRenewalFlag=$spgroup[11];
				$spgprepos=$spgroup[12];

				if($spgrows>0)
				{
					$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunenumber='$spgtunenumber' and tunetype='$spgtunetype'");
					$str->execute;
					$MTRcomment=$str->fetchrow();
					$str->finish();
					$mysql->disconnect();

					$MTRcomment="$MTRcomment : CLI $spgassignto";

					$mysql->do("update existnewsubscriber set assignto='$spgassignto',groupnumber='$spggrpnumber',tunenumber='$spgtunenumber',tunetype='$spgtunetype',date='$spgdate',expdate='$spgexpdate',activate='$spgactivate',subcriptiontype='$spgsubtype',subtypename='$spgsubtypename',serverid='$spgserverid',userstatus='$spguserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',prepos='$spgprepos' where mobno='$mobno'");
					$mysql->do("insert into existnewsubscribermis (mobno,assignto,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,prepos) values ('$mobno','$spgassignto','$spgtunenumber','$spgtunetype','$spgdate','$spgexpdate','$spgactivate','$spgsubtype','$spgsubtypename','$spgserverid','$spguserstatus',1,2,'$MTRcomment','$spgprepos')");
					$flag=1;
					last;
				}
				else { next; }
			}
			elsif($table eq "spcaller")
			{
				$str=$mysql->prepare("select assignto,tunenumber,tunetype,date,expdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,prepos from spcaller where mobno='$mobno' and mobno<>assignto and groupnumber=0 and playdate + INTERVAL 7 DAY > curdate() and activate=1 order by date desc limit 1");
				$str->execute;
				@spcaller=$str->fetchrow();
				$spcrows=$str->rows;
				$str->finish();

				$spcassignto=$spcaller[0];
				$spctunenumber=$spcaller[1];
				$spctunetype=$spcaller[2];
				$spcdate=$spcaller[3];
				$spcexpdate=$spcaller[4];
				$spcactivate=$spcaller[5];
				$spcuserstatus=$spcaller[6];
				$spcsubtype=$spcaller[7];
				$spcsubtypename=$spcaller[8];
				$spcserverid=$spcaller[9];
				$spcRenewalFlag=$spcaller[10];
				$spcprepos=$spcaller[11];

				if($spcrows>0)
				{
					$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunenumber='$spctunenumber' and tunetype='$spctunetype'");
					$str->execute;
					$MTRcomment=$str->fetchrow();
					$str->finish();
					$mysql->disconnect();

					$MTRcomment="$MTRcomment : CLI $spcassignto";

					$mysql->do("update existnewsubscriber set assignto='$spcassignto',tunenumber='$spctunenumber',tunetype='$spctunetype',date='$spcdate',expdate='$spcexpdate',activate='$spcactivate',subcriptiontype='$spcsubtype',subtypename='$spcsubtypename',serverid='$spcserverid',userstatus='$spcuserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',prepos='$spcprepos' where mobno='$mobno'");
					$mysql->do("insert into existnewsubscribermis (mobno,assignto,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,prepos) values ('$mobno','$spcassignto','$spctunenumber','$spctunetype','$spcdate','$spcexpdate','$spcactivate','$spcsubtype','$spcsubtypename','$spcserverid','$spcuserstatus',1,2,'$MTRcomment','$spcprepos')");
					$flag=1;
					last;
				}
				else { next; }
			}
			elsif($table eq "sptime")
			{
				$str=$mysql->prepare("select tunenumber,tunetype,date,expdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,prepos from sptime where mobno='$mobno' and playdate + INTERVAL 7 DAY > curdate() and activate=1 order by date desc limit 1");
				$str->execute;
				@sptime=$str->fetchrow();
				$sptrows=$str->rows;
				$str->finish();

				$spttunenumber=$sptime[0];
				$spttunetype=$sptime[1];
				$sptdate=$sptime[2];
				$sptexpdate=$sptime[3];
				$sptactivate=$sptime[4];
				$sptuserstatus=$sptime[5];
				$sptsubtype=$sptime[6];
				$sptsubtypename=$sptime[7];
				$sptserverid=$sptime[8];
				$sptRenewalFlag=$sptime[9];
				$sptprepos=$sptime[10];

				if($sptrows>0)
				{
					$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunenumber='$spttunenumber' and tunetype='$spttunetype'");
					$str->execute;
					$MTRcomment=$str->fetchrow();
					$str->finish();
					$mysql->disconnect();

					$mysql->do("update existnewsubscriber set tunenumber='$spttunenumber',tunetype='$spttunetype',date='$sptdate',expdate='$sptexpdate',activate='$sptactivate',subcriptiontype='$sptsubtype',subtypename='$sptsubtypename',serverid='$sptserverid',userstatus='$sptuserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',prepos='$sptprepos' where mobno='$mobno'");
					$mysql->do("insert into existnewsubscribermis (mobno,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,prepos) values ('$mobno','$spttunenumber','$spttunetype','$sptdate','$sptexpdate','$sptactivate','$sptsubtype','$sptsubtypename','$sptserverid','$sptuserstatus',1,2,'$MTRcomment','$sptprepos')");
					$flag=1;
					last;
				}
				else { next; }
			}
			elsif($table eq "tunepack")
			{
				$str=$mysql->prepare("select p.tpnumber,p.tptype,t.date,t.expdate,t.activate,t.userstatus,t.subcriptiontype,t.subtypename,t.serverid,t.RenewalFlag,p.contprov,t.prepos from tunepack t,tunepacktunes p where t.mobno='$mobno' and t.TuneSN=p.tpnumber and t.tunenumber=p.tunenumber and t.tunetype=p.tunetype and t.playdate + INTERVAL 7 DAY > curdate() and t.activate=1 order by t.date desc limit 1");
				$str->execute;
				@tunepack=$str->fetchrow();
				$tprows=$str->rows;
				$str->finish();

				$tptunenumber=$tunepack[0];
				$tptunetype=$tunepack[1];
				$tpdate=$tunepack[2];
				$tpexpdate=$tunepack[3];
				$tpactivate=$tunepack[4];
				$tpuserstatus=$tunepack[5];
				$tpsubtype=$tunepack[6];
				$tpsubtypename=$tunepack[7];
				$tpserverid=$tunepack[8];
				$tpRenewalFlag=$tunepack[9];
				$tcp=$tunepack[10];
				$tpprepos=$tunepack[11];

				if($tprows>0)
				{
					$MTRcomment="CRBT SN $tptunenumber M P $tcp";

					$mysql->do("update existnewsubscriber set tunenumber='$tptunenumber',tunetype='$tptunetype',date='$tpdate',expdate='$tpexpdate',activate='$tptactivate',subcriptiontype='$tpsubtype',subtypename='$tpsubtypename',serverid='$tpserverid',userstatus='$tpuserstatus',billed=1,HTservice=1,MTRcomment='$MTRcomment',prepos='$tpprepos' where mobno='$mobno'");
					$mysql->do("insert into existnewsubscribermis (mobno,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,prepos) values ('$mobno','$tptunenumber','$tptunetype','$tpdate','$tpexpdate','$tpactivate','$tpsubtype','$tpsubtypename','$tpserverid','$tpuserstatus',1,1,'$MTRcomment','$tpprepos')");
					$flag=1;
					last;
				}
				else { next; }
			}
			elsif($table eq "gift")
			{
				$str=$mysql->prepare("select assignto,tunenumber,tunetype,date,expdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,prepos from gift where activate=1 and mobno='$mobno' order by date desc limit 1");
				$str->execute;
				@gifttune=$str->fetchrow();
				$gtrows=$str->rows;
				$str->finish();

				$gtassignto=$gifttune[0];
				$gttunenumber=$gifttune[1];
				$gttunetype=$gifttune[2];
				$gtdate=$gifttune[3];
				$gtexpdate=$gifttune[4];
				$gtactivate=$gifttune[5];
				$gtuserstatus=$gifttune[6];
				$gtsubtype=$gifttune[7];
				$gtsubtypename=$gifttune[8];
				$gtserverid=$gifttune[9];
				$gtRenewalFlag=$gifttune[10];
				$gtprepos=$gifttune[11];

				if($gtrows>0)
				{
					$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunenumber='$gttunenumber' and tunetype='$gttunetype'");
					$str->execute;
					$MTRcomment=$str->fetchrow();
					$str->finish();
					$mysql->disconnect();

					$MTRcomment="$MTRcomment : GIFT $gtassignto";

					$mysql->do("update existnewsubscriber set assignto='$gtassignto',tunenumber='$gttunenumber',tunetype='$gttunetype',date='$gtdate',expdate='$gtexpdate',activate='$gtactivate',subcriptiontype='$gtsubtype',subtypename='$gtsubtypename',serverid='$gtserverid',userstatus='$gtuserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',prepos='$gtprepos' where mobno='$mobno'");
					$mysql->do("insert into existnewsubscribermis (mobno,assignto,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,prepos) values ('$mobno','$gtassignto','$gttunenumber','$gttunetype','$gtdate','$gtexpdate','$gtactivate','$gtsubtype','$gtsubtypename','$gtserverid','$gtuserstatus',1,2,'$MTRcomment','$gtprepos')");
					$flag=1;
					last;
				}
				else { next; }
			}
		}
		$mysql->do("insert into deactivated (mobno,lang,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno','$lang',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");
		if($flag==0)
		{
			$mysql->do("update existnewsubscriber set date=now(),activate=2,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',HTservice=2,prepos='$prepos' where mobno='$mobno'");
			$mysql->do("insert into existnewsubscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid,HTservice,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid',2,'$prepos')");
		}
	}

	$mysql->disconnect();
}


sub HTY
{
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from HTYPOSTPAIDOBDpromotion where mobno='$mobno' and DATEDIFF(expdate,curdate()) in (0,1) and activate=0 and topick=0");
	$str->execute;
	$pcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($pcount==1)
	{
		&HTYPOSTPAIDOBDpromotion;
	}
	else
	{
		$dsql=DBI->connect($dsnd,$dbuser,$dbpasswd);
		$str=$dsql->prepare("select count(*) from MANSMSOBDpromobase_20Jan2015 where mobno='$mobno' and DATEDIFF(curdate(),date(date)) in (0,1,2,3,4) and activate<>9");
		$str->execute;
		$ncount=$str->fetchrow();
		$str->finish();
		$dsql->disconnect();

		if($ncount==1)
		{
			&HTYNonUserPromotion;
		}
		else
		{
			#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

			$userstatus='E';

			$MsgID="1077";
			&SendConfSMS;

			exit;
		}
	}
}


sub HTYPOSTPAIDOBDpromotion
{
#################################################### HT Y POSTPAIDOBD Promotion -- Start ####################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select tunenumber,tunetype,activate,response,subcriptiontype,subtypename,serverid,promoid,topick,prepos from HTYPOSTPAIDOBDpromotion where mobno='$mobno'");
	$str->execute;
	@arr=$str->fetchrow();
	$count=$str->rows;
	$str->finish();
	$mysql->disconnect();

	$tunenumber=$arr[0];
	$tunetype=$arr[1];
	$activate=$arr[2];
	$message=$arr[3];
	$subcriptiontype=$arr[4];
	$subtypename=$arr[5];
	$sid=$arr[6];
	$promoid=$arr[7];
	$topick=$arr[8];
	$prepos=$arr[9];

	$userstatus='E';

	if($count==1)
	{
		if($message eq "Z")
		{
			if($activate==1)
			{
				$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

				$str=$mysql->prepare("select count(*) from subscriber where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1 and freetune=2 and promoid='$promoid'");
				$str->execute;
				$subscnt=$str->fetchrow();
				$str->finish();

				$str=$mysql->prepare("select count(*) from jukebox where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1 and freetune=2 and promoid='$promoid'");
				$str->execute;
				$jukecnt=$str->fetchrow();
				$str->finish();
				
				$mysql->disconnect();

				if($subscnt==1 || $jukecnt==1)
				{
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$mysql->do("update subscriber set freetune=1,date=now() where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and freetune=2 and promoid='$promoid'");
					$mysql->do("update jukebox set freetune=1,date=now() where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and freetune=2 and promoid='$promoid'");

					$mysql->do("update HTYPOSTPAIDOBDpromotion set date=now(),response='Y' where mobno='$mobno'");

					$mysql->disconnect();

					#$message="Your Free Tune is now activated! Thank you. Hutch";

					$MsgID="1074";
					&SendConfSMS;

					exit;
				}
			}
			elsif($activate==3)
			{
				#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

				$MsgID="1077";
				&SendConfSMS;

				exit;
			}
		}
		elsif($message eq "Y")
		{
			#$message="Your Free Tune is already activated! Thank you. Hutch";

			$MsgID="1075";
			&SendConfSMS;

			exit;
		}
		elsif($message eq "N")
		{
			#$message="Your Free Tune is already deactivated! Thank you. Hutch";

			$MsgID="1076";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

		$MsgID="1077";
		&SendConfSMS;

		exit;
	}

##################################################### HT Y POSTPAIDOBD Promotion -- End #####################################################

}


sub HTYNonUserPromotion
{
##################################################### HT Y Non User Promotion -- Start ######################################################

	$dsql=DBI->connect($dsnd,$dbuser,$dbpasswd);
	$str=$dsql->prepare("select tunenumber,tunetype,activate,subcriptiontype,subtypename,serverid,userstatus,topick,response,status from MANSMSOBDpromobase_20Jan2015 where mobno='$mobno'");
	$str->execute;
	@arr=$str->fetchrow();
	$count=$str->rows;
	$str->finish();
	$dsql->disconnect();

	$tunenumber=$arr[0];
	$tunetype=$arr[1];
	$activate=$arr[2];
	$subcriptiontype=$arr[3];
	$subtypename=$arr[4];
	$sid=$arr[5];
	$userstatus=$arr[6];
	$topick=$arr[7];
	$message=$arr[8];
	$status=$arr[9];

	$promoid="452";

	if($count==1)
	{
		if($message eq "Z")
		{
			if($activate==1)
			{
				if($status>=0 && $status<=3)
				{
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$str=$mysql->prepare("select count(*) from subscriber where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1 and freetune=2 and promoid='$promoid'");
					$str->execute;
					$subscnt=$str->fetchrow();
					$str->finish();

					$str=$mysql->prepare("select count(*) from jukebox where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1 and freetune=2 and promoid='$promoid'");
					$str->execute;
					$jukecnt=$str->fetchrow();
					$str->finish();

					$mysql->disconnect();

					if($subscnt==1 || $jukecnt==1)
					{
						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

						$mysql->do("update subscriber set freetune=1,date=now() where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and freetune=2 and promoid='$promoid'");
						$mysql->do("update jukebox set freetune=1,date=now() where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and freetune=2 and promoid='$promoid'");

						$mysql->disconnect();

						$dsql=DBI->connect($dsnd,$dbuser,$dbpasswd);
						$dsql->do("update MANSMSOBDpromobase_20Jan2015 set date=now(),response='Y' where mobno='$mobno'");
						$dsql->disconnect();

						#$message="Your Free Tune is now activated! Thank you. Hutch";

						$MsgID="1074";
						&SendConfSMS;

						exit;
					}
				}
			}
			elsif($activate==3)
			{
				#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

				$MsgID="1077";
				&SendConfSMS;

				exit;
			}
			elsif($activate==2)
			{
				#$message="Your Free Tune is already deactivated! Thank you. Hutch";

				$MsgID="1076";
				&SendConfSMS;

				exit;
			}
		}
		elsif($message eq "Y")
		{
			#$message="Your Free Tune is already activated! Thank you. Hutch";

			$MsgID="1075";
			&SendConfSMS;

			exit;
		}
		elsif($message eq "N")
		{
			#$message="Your Free Tune is already deactivated! Thank you. Hutch";

			$MsgID="1076";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

		$MsgID="1077";
		&SendConfSMS;

		exit;
	}

###################################################### HT Y Non User Promotion -- End #######################################################

}


sub HTN
{
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from NewAcqusitionpromotion where mobno='$mobno' and DATEDIFF(expdate,curdate()) in (1,2,3,4,5,6,7) and activate=1 and topick=1 and response='Z' and promoid in(133,173)");
	$str->execute;
	$ncount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($ncount==1)
	{
		&NEWACQUISITIONpromotion;
	}
	else
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$str=$mysql->prepare("select count(*) from HTNPOSTPAIDOBDpromotion where mobno='$mobno' and DATEDIFF(expdate,curdate()) in (0,1) and activate=0 and topick=0");
		$str->execute;
		$pcount=$str->fetchrow();
		$str->finish();
		$mysql->disconnect();

		if($pcount==1)
		{
			&HTNPOSTPAIDOBDpromotion;
		}
		else
		{
			$dsql=DBI->connect($dsnd,$dbuser,$dbpasswd);
			$str=$dsql->prepare("select count(*) from MANSMSOBDpromobase_20Jan2015 where mobno='$mobno' and DATEDIFF(curdate(),date(date)) in (0,1,2,3,4) and activate<>9");
			$str->execute;
			$ncount=$str->fetchrow();
			$str->finish();
			$dsql->disconnect();

			if($ncount==1)
			{
				&HTNNonUserPromotion;
			}
			else
			{
				#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

				$MsgID="1077";
				&SendConfSMS;

				exit;
			}
		}
	}
}


sub NEWACQUISITIONpromotion
{
#################################################### NewAcquisition  Promotion -- Start ###################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select tunenumber,tunetype,activate,response,subcriptiontype,subtypename,serverid,promoid,topick,prepos from NewAcqusitionpromotion where mobno='$mobno'");
	$str->execute;
	@arr=$str->fetchrow();
	$count=$str->rows;
	$str->finish();
	$mysql->disconnect();

	$tunenumber=$arr[0];
	$tunetype=$arr[1];
	$activate=$arr[2];
	$message=$arr[3];
	$subcriptiontype=$arr[4];
	$subtypename=$arr[5];
	$sid=$arr[6];
	$promoid=$arr[7];
	$topick=$arr[8];
	$prepos=$arr[9];

	$userstatus='E';

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),HTservice from existnewsubscriber where mobno='$mobno' group by mobno");
	$str->execute;
	@arr=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$nesubscnt=$arr[0];
	$HTservice=$arr[1];

	if($nesubscnt==0)
	{
		#$message="You are not a subscriber of HelloTunes. To Activate the Service please call 369. Charges Apply.";

		$userstatus='E';

		$MsgID="1079";
		&SendConfSMS;

		exit;
	}

	if($count==1 && $nesubscnt==1)
	{
		if($activate==1)
		{
			if($message eq "Z")
			{
				$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

				$str=$mysql->prepare("select count(*),JKflag from subscriber where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1 and freetune=1 and promoid='$promoid'");
				$str->execute;
				@subs=$str->fetchrow();
				$str->finish();

				$sfreecnt=$subs[0];
				$JKflag=$subs[1];

				$str=$mysql->prepare("select count(*) from jukebox where mobno='$mobno' and activate=1");
				$str->execute;
				$jukecnt=$str->fetchrow();
				$str->finish();

				$str=$mysql->prepare("select sno,tunenumber,tunetype,deftune,TuneSN,userstatus from jukebox where mobno='$mobno' and activate=1 and freetune=1 and promoid='$promoid'");
				$str->execute();
				@juke=$str->fetchrow();
				$jfreecnt=$str->rows;
				$str->finish();

				$mysql->disconnect();

				$sno=$juke[0];
				$juketuneno=$juke[1];
				$juketunety=$juke[2];
				$deftune=$juke[3];
				$TuneSN=$juke[4];
				$jukeuserstatus=$juke[5];

				if($sfreecnt==1 && $JKflag==0)
				{
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$mysql->do("delete from subscriber where mobno='$mobno'");
					$mysql->do("insert into subscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");

					$mysql->disconnect();

					&OtherFeatures;

				update:
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
					$mysql->do("update NewAcqusitionpromotion set date=now(),response='N' where mobno='$mobno'");
					$mysql->do("insert into deactivated (mobno,lang,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno','$lang',now(),2,'$subcriptiontype','$subtypename','$sid')");
					$mysql->disconnect();

					#$message="Ur FREE TUNE is now deactivated free of charge. For more hellotunes call 369.";

					$MsgID="1080";
					&SendConfSMS;

					exit;
				}
				elsif(($sfreecnt==1 && $JKflag==1) || $jfreecnt==1)
				{
					if($jukecnt==1)
					{
						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

						$mysql->do("delete from subscriber where mobno='$mobno'");
						$mysql->do("insert into subscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");

						$mysql->do("delete from jukebox where mobno='$mobno'");
						$mysql->do("insert into jukeboxmis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");

						$mysql->disconnect();

						goto update;
					}

					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$str=$mysql->prepare("select sno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag from jukebox where mobno='$mobno' and activate=1 and promoid<>'$promoid' order by sdate desc limit 1");
					$str->execute;
					@juketunes=$str->fetchrow();
					$str->finish();

					$mysql->disconnect();

					$jksno=$juketunes[0];
					$jktuneno=$juketunes[1];
					$jktunety=$juketunes[2];
					$jkdate=$juketunes[3];
					$jkexpdate=$juketunes[4];
					$jksdate=$juketunes[5];
					$jkplaydate=$juketunes[6];
					$jkactivate=$juketunes[7];
					$jkuserstatus=$juketunes[8];
					$jksubtype=$juketunes[9];
					$jksubtyname=$juketunes[10];
					$jksid=$juketunes[11];
					$jkRenewalFlag=$juketunes[12];
					$jkfreetune=$juketunes[13];
					$jkpromoid=$juketunes[14];
					$jkprepos=$juketunes[15];
					$jkARBflag=$juketunes[16];

					if($jukecnt==2)
					{
						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

						$mysql->do("update subscriber set tunenumber='$jktuneno',tunetype='$jktunety',date='$jkdate',expdate='$jkexpdate',sdate='$jksdate',playdate='$jkplaydate',activate='$jkactivate',JKflag=0,userstatus='$jkuserstatus',subcriptiontype='$jksubtype',subtypename='$jksubtyname',serverid='$jksid',RenewalFlag='$jkRenewalFlag',freetune='$jkfreetune',promoid='$jkpromoid',prepos='$jkprepos',ARBflag='$jkARBflag' where mobno='$mobno'");
						$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$jktuneno','$jktunety','$jkdate','$jkexpdate','$jksdate','$jkplaydate','$jkactivate',1,'$jkuserstatus','$jksubtype','$jksubtyname','$jksid','$jkRenewalFlag','$jkfreetune','$jkpromoid','$jkprepos','$jkARBflag')");

						$mysql->do("delete from jukebox where mobno='$mobno'");
						$mysql->do("insert into jukeboxmis(mobno,tunenumber,tunetype,date,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid) values ('$mobno','$juketuneno','$juketunety',now(),2,'$TuneSN','$jukeuserstatus','$subcriptiontype','$subtypename','$sid')");

						$mysql->disconnect();

						goto update;
					}
					elsif($jukecnt>2)
					{
						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

						$mysql->do("delete from jukebox where sno='$sno'");

						if($deftune==1)
						{
							$mysql->do("update jukebox set deftune=0 where mobno='$mobno'");
							$mysql->do("update jukebox set deftune=1 where sno='$jksno'");

							$mysql->do("update subscriber set tunenumber='$jktuneno',tunetype='$jktunety',date='$jkdate',expdate='$jkexpdate',sdate='$jksdate',playdate='$jkplaydate',activate='$jkactivate',JKflag=1,userstatus='$jkuserstatus',subcriptiontype='$jksubtype',subtypename='$jksubtyname',serverid='$jksid',RenewalFlag='$jkRenewalFlag',freetune='$jkfreetune',promoid='$jkpromoid',prepos='$jkprepos',ARBflag='$jkARBflag' where mobno='$mobno'");
							$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$jktuneno','$jktunety','$jkdate','$jkexpdate','$jksdate','$jkplaydate','$jkactivate',1,'$jkuserstatus','$jksubtype','$jksubtyname','$jksid','$jkRenewalFlag','$jkfreetune','$jkpromoid','$jkprepos','$jkARBflag')");
						}

						$maxsno=$maxsno-1;
						$mysql->do("update jukebox set TuneSN=TuneSN-1 where TuneSN>'$TuneSN' and mobno='$mobno'");
						$mysql->do("insert into jukeboxmis(mobno,tunenumber,tunetype,date,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid) values ('$mobno','$juketuneno','$juketunety',now(),2,'$TuneSN','$jukeuserstatus','$subcriptiontype','$subtypename','$sid')");

						$mysql->disconnect();

						goto update;
					}

					&OtherFeatures;

				update:
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
					$mysql->do("update NewAcqusitionpromotion set date=now(),response='N' where mobno='$mobno'");
					$mysql->do("insert into deactivated (mobno,lang,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno','$lang',now(),2,'$subcriptiontype','$subtypename','$sid')");
					$mysql->disconnect();

					#$message="Ur FREE TUNE is now deactivated free of charge. For more hellotunes call 369.";

					$MsgID="1080";
					&SendConfSMS;

					exit;
				}
				else
				{
					#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

					$MsgID="1077";
					&SendConfSMS;

					exit;
				}
			}
			elsif($message eq "Y")
			{
				#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

				$MsgID="1077";
				&SendConfSMS;

				exit;
			}
		}
		elsif($activate==2)
		{
			#$message="Your Free Tune is already deactivated! Thank you. Hutch";

			$MsgID="1081";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

		$MsgID="1077";
		&SendConfSMS;

		exit;
	}

#################################################### NewAcquisition Promotion -- end #######################################

}


sub HTNPOSTPAIDOBDpromotion
{
############################################### HT N POSTPAIDOBD Promotion -- Start ##############################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select tunenumber,tunetype,activate,response,subcriptiontype,subtypename,serverid,promoid,topick,prepos from HTNPOSTPAIDOBDpromotion where mobno='$mobno'");
	$str->execute;
	@arr=$str->fetchrow();
	$count=$str->rows;
	$str->finish();
	$mysql->disconnect();

	$tunenumber=$arr[0];
	$tunetype=$arr[1];
	$activate=$arr[2];
	$message=$arr[3];
	$subcriptiontype=$arr[4];
	$subtypename=$arr[5];
	$sid=$arr[6];
	$promoid=$arr[7];
	$topick=$arr[8];
	$prepos=$arr[9];

	$userstatus='E';

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),HTservice from existnewsubscriber where mobno='$mobno' group by mobno");
	$str->execute;
	@arr=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$nesubscnt=$arr[0];
	$HTservice=$arr[1];

	if($nesubscnt==0)
	{
		#$message="You are not a subscriber of HelloTunes. To Activate the Service please call 369. Charges Apply.";

		$userstatus='E';

		$MsgID="1079";
		&SendConfSMS;

		exit;
	}

	if($count==1 && $nesubscnt==1)
	{
		if($activate==1)
		{
			if($message eq "Z")
			{
				$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

				$str=$mysql->prepare("select count(*),JKflag from subscriber where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1 and freetune=2 and promoid='$promoid'");
				$str->execute;
				@subs=$str->fetchrow();
				$str->finish();

				$sfreecnt=$subs[0];
				$JKflag=$subs[1];

				$str=$mysql->prepare("select count(*) from jukebox where mobno='$mobno' and activate=1");
				$str->execute;
				$jukecnt=$str->fetchrow();
				$str->finish();

				$str=$mysql->prepare("select sno,tunenumber,tunetype,deftune,TuneSN,userstatus from jukebox where mobno='$mobno' and activate=1 and freetune=2 and promoid='$promoid'");
				$str->execute();
				@juke=$str->fetchrow();
				$jfreecnt=$str->rows;
				$str->finish();

				$mysql->disconnect();

				$sno=$juke[0];
				$juketuneno=$juke[1];
				$juketunety=$juke[2];
				$deftune=$juke[3];
				$TuneSN=$juke[4];
				$jukeuserstatus=$juke[5];

				if($sfreecnt==1 && $JKflag==0)
				{
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$mysql->do("delete from subscriber where mobno='$mobno'");
					$mysql->do("insert into subscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");

					$mysql->disconnect();
				}
				elsif(($sfreecnt==1 && $JKflag==1) || $jfreecnt==1)
				{
					if($jukecnt==1)
					{
						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

						$mysql->do("delete from subscriber where mobno='$mobno'");
						$mysql->do("insert into subscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");

						$mysql->do("delete from jukebox where mobno='$mobno'");
						$mysql->do("insert into jukeboxmis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");

						$mysql->disconnect();

						goto update;
					}

					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$str=$mysql->prepare("select sno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag from jukebox where mobno='$mobno' and activate=1 and freetune<>2 order by sdate desc limit 1");
					$str->execute;
					@juketunes=$str->fetchrow();
					$str->finish();

					$mysql->disconnect();

					$jksno=$juketunes[0];
					$jktuneno=$juketunes[1];
					$jktunety=$juketunes[2];
					$jkdate=$juketunes[3];
					$jkexpdate=$juketunes[4];
					$jksdate=$juketunes[5];
					$jkplaydate=$juketunes[6];
					$jkactivate=$juketunes[7];
					$jkuserstatus=$juketunes[8];
					$jksubtype=$juketunes[9];
					$jksubtyname=$juketunes[10];
					$jksid=$juketunes[11];
					$jkRenewalFlag=$juketunes[12];
					$jkfreetune=$juketunes[13];
					$jkpromoid=$juketunes[14];
					$jkprepos=$juketunes[15];
					$jkARBflag=$juketunes[16];

					if($jukecnt==2)
					{
						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

						$mysql->do("update subscriber set tunenumber='$jktuneno',tunetype='$jktunety',date='$jkdate',expdate='$jkexpdate',sdate='$jksdate',playdate='$jkplaydate',activate='$jkactivate',JKflag=0,userstatus='$jkuserstatus',subcriptiontype='$jksubtype',subtypename='$jksubtyname',serverid='$jksid',RenewalFlag='$jkRenewalFlag',freetune='$jkfreetune',promoid='$jkpromoid',prepos='$jkprepos',ARBflag='$jkARBflag' where mobno='$mobno'");
						$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$jktuneno','$jktunety','$jkdate','$jkexpdate','$jksdate','$jkplaydate','$jkactivate',1,'$jkuserstatus','$jksubtype','$jksubtyname','$jksid','$jkRenewalFlag','$jkfreetune','$jkpromoid','$jkprepos','$jkARBflag')");

						$mysql->do("delete from jukebox where mobno='$mobno'");
						$mysql->do("insert into jukeboxmis(mobno,tunenumber,tunetype,date,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid) values ('$mobno','$juketuneno','$juketunety',now(),2,'$TuneSN','$jukeuserstatus','$subcriptiontype','$subtypename','$sid')");

						$mysql->disconnect();

						goto update;
					}
					elsif($jukecnt>2)
					{
						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

						$mysql->do("delete from jukebox where sno='$sno'");

						if($deftune==1)
						{
							$mysql->do("update jukebox set deftune=0 where mobno='$mobno'");
							$mysql->do("update jukebox set deftune=1 where sno='$jksno'");

							$mysql->do("update subscriber set tunenumber='$jktuneno',tunetype='$jktunety',date='$jkdate',expdate='$jkexpdate',sdate='$jksdate',playdate='$jkplaydate',activate='$jkactivate',JKflag=1,userstatus='$jkuserstatus',subcriptiontype='$jksubtype',subtypename='$jksubtyname',serverid='$jksid',RenewalFlag='$jkRenewalFlag',freetune='$jkfreetune',promoid='$jkpromoid',prepos='$jkprepos',ARBflag='$jkARBflag' where mobno='$mobno'");
							$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$jktuneno','$jktunety','$jkdate','$jkexpdate','$jksdate','$jkplaydate','$jkactivate',1,'$jkuserstatus','$jksubtype','$jksubtyname','$jksid','$jkRenewalFlag','$jkfreetune','$jkpromoid','$jkprepos','$jkARBflag')");
						}

						$maxsno=$maxsno-1;
						$mysql->do("update jukebox set TuneSN=TuneSN-1 where TuneSN>'$TuneSN' and mobno='$mobno'");
						$mysql->do("insert into jukeboxmis(mobno,tunenumber,tunetype,date,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid) values ('$mobno','$juketuneno','$juketunety',now(),2,'$TuneSN','$jukeuserstatus','$subcriptiontype','$subtypename','$sid')");

						$mysql->disconnect();

						goto update;
					}

					&OtherFeatures;

				update:
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
					$mysql->do("update HTNPOSTPAIDOBDpromotion set date=now(),response='N' where mobno='$mobno'");
					$mysql->do("insert into deactivated (mobno,lang,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno','$lang',now(),2,'$subcriptiontype','$subtypename','$sid')");
					$mysql->disconnect();

					#$message="Ur FREE TUNE is now deactivated free of charge. For more hellotunes call 369.";

					$MsgID="1080";
					&SendConfSMS;

					exit;
				}
				else
				{
					#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

					$MsgID="1082";
					&SendConfSMS;

					exit;
				}
			}
			elsif($message eq "Y")
			{
				#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

				$MsgID="1082";
				&SendConfSMS;

				exit;
			}
		}
		elsif($activate==2)
		{
			#$message="Your Free Tune is already deactivated! Thank you. Hutch";

			$MsgID="1081";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

		$MsgID="1077";
		&SendConfSMS;

		exit;
	}

############################################### HT N POSTPAIDOBD Promotion -- End ################################################

}


sub HTNNonUserPromotion
{
############################################### HT N Non User Promotion -- Start #################################################

	$dsql=DBI->connect($dsnd,$dbuser,$dbpasswd);
	$str=$dsql->prepare("select tunenumber,tunetype,activate,subcriptiontype,subtypename,serverid,userstatus,topick,response,status from MANSMSOBDpromobase_20Jan2015 where mobno='$mobno'");
	$str->execute;
	@arr=$str->fetchrow();
	$count=$str->rows;
	$str->finish();
	$dsql->disconnect();

	$tunenumber=$arr[0];
	$tunetype=$arr[1];
	$activate=$arr[2];
	$subcriptiontype=$arr[3];
	$subtypename=$arr[4];
	$sid=$arr[5];
	$userstatus=$arr[6];
	$topick=$arr[7];
	$message=$arr[8];
	$status=$arr[9];

	$promoid="452";

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),HTservice from existnewsubscriber where mobno='$mobno' group by mobno");
	$str->execute;
	@arr=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$nesubscnt=$arr[0];
	$HTservice=$arr[1];

	if($nesubscnt==0)
	{
		#$message="You are not a subscriber of HelloTunes. To Activate the Service please call 369. Charges Apply.";

		$userstatus='E';

		$MsgID="1079";
		&SendConfSMS;

		exit;
	}

	if($count==1 && $nesubscnt==1)
	{
		if($activate==1)
		{
			if($message eq "Z")
			{
				if($status>=0 && $status<=3)
				{
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$str=$mysql->prepare("select count(*),JKflag from subscriber where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1 and freetune=2 and promoid='$promoid'");
					$str->execute;
					@subs=$str->fetchrow();
					$str->finish();

					$sfreecnt=$subs[0];
					$JKflag=$subs[1];

					$str=$mysql->prepare("select count(*) from jukebox where mobno='$mobno' and activate=1");
					$str->execute;
					$jukecnt=$str->fetchrow();
					$str->finish();

					$str=$mysql->prepare("select sno,tunenumber,tunetype,deftune,TuneSN,userstatus from jukebox where mobno='$mobno' and activate=1 and freetune=2 and promoid='$promoid'");
					$str->execute();
					@juke=$str->fetchrow();
					$jfreecnt=$str->rows;
					$str->finish();

					$mysql->disconnect();

					$sno=$juke[0];
					$juketuneno=$juke[1];
					$juketunety=$juke[2];
					$deftune=$juke[3];
					$TuneSN=$juke[4];
					$jukeuserstatus=$juke[5];

					if($sfreecnt==1 && $JKflag==0)
					{
						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
						$mysql->do("delete from subscriber where mobno='$mobno'");
						$mysql->do("insert into subscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");
						$mysql->disconnect();

						&OtherFeatures;

						$dsql=DBI->connect($dsnd,$dbuser,$dbpasswd);
						$dsql->do("update MANSMSOBDpromobase_20Jan2015 set date=now(),activate=2,response='N' where mobno='$mobno'");
						$dsql->disconnect();

						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
						$mysql->do("insert into deactivated (mobno,lang,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno','$lang',now(),2,'$subcriptiontype','$subtypename','$sid')");
						$mysql->disconnect();


						#$message="Ur FREE TUNE is now deactivated free of charge. For more hellotunes call 369.";

						$MsgID="1080";
						&SendConfSMS;

						exit;
					}
					elsif(($sfreecnt==1 && $JKflag==1) || $jfreecnt==1)
					{
						if($jukecnt==1)
						{
							$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

							$mysql->do("delete from subscriber where mobno='$mobno'");
							$mysql->do("insert into subscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");

							$mysql->do("delete from jukebox where mobno='$mobno'");
							$mysql->do("insert into jukeboxmis(mobno,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid')");

							$mysql->disconnect();

							goto update;
						}

						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

						$str=$mysql->prepare("select sno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag from jukebox where mobno='$mobno' and activate=1 and promoid<>'$promoid' order by sdate desc limit 1");
						$str->execute;
						@juketunes=$str->fetchrow();
						$str->finish();

						$mysql->disconnect();

						$jksno=$juketunes[0];
						$jktuneno=$juketunes[1];
						$jktunety=$juketunes[2];
						$jkdate=$juketunes[3];
						$jkexpdate=$juketunes[4];
						$jksdate=$juketunes[5];
						$jkplaydate=$juketunes[6];
						$jkactivate=$juketunes[7];
						$jkuserstatus=$juketunes[8];
						$jksubtype=$juketunes[9];
						$jksubtyname=$juketunes[10];
						$jksid=$juketunes[11];
						$jkRenewalFlag=$juketunes[12];
						$jkfreetune=$juketunes[13];
						$jkpromoid=$juketunes[14];
						$jkprepos=$juketunes[15];
						$jkARBflag=$juketunes[16];

						if($jukecnt==2)
						{
							$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

							$mysql->do("update subscriber set tunenumber='$jktuneno',tunetype='$jktunety',date='$jkdate',expdate='$jkexpdate',sdate='$jksdate',playdate='$jkplaydate',activate='$jkactivate',JKflag=0,userstatus='$jkuserstatus',subcriptiontype='$jksubtype',subtypename='$jksubtyname',serverid='$jksid',RenewalFlag='$jkRenewalFlag',freetune='$jkfreetune',promoid='$jkpromoid',prepos='$jkprepos',ARBflag='$jkARBflag' where mobno='$mobno'");
							$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$jktuneno','$jktunety','$jkdate','$jkexpdate','$jksdate','$jkplaydate','$jkactivate',1,'$jkuserstatus','$jksubtype','$jksubtyname','$jksid','$jkRenewalFlag','$jkfreetune','$jkpromoid','$jkprepos','$jkARBflag')");

							$mysql->do("delete from jukebox where mobno='$mobno'");
							$mysql->do("insert into jukeboxmis(mobno,tunenumber,tunetype,date,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid) values ('$mobno','$juketuneno','$juketunety',now(),2,'$TuneSN','$jukeuserstatus','$subcriptiontype','$subtypename','$sid')");

							$mysql->disconnect();

							goto update;
						}
						elsif($jukecnt>2)
						{
							$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

							$mysql->do("delete from jukebox where sno='$sno'");

							if($deftune==1)
							{
								$mysql->do("update jukebox set deftune=0 where mobno='$mobno'");
								$mysql->do("update jukebox set deftune=1 where sno='$jksno'");

								$mysql->do("update subscriber set tunenumber='$jktuneno',tunetype='$jktunety',date='$jkdate',expdate='$jkexpdate',sdate='$jksdate',playdate='$jkplaydate',activate='$jkactivate',JKflag=1,userstatus='$jkuserstatus',subcriptiontype='$jksubtype',subtypename='$jksubtyname',serverid='$jksid',RenewalFlag='$jkRenewalFlag',freetune='$jkfreetune',promoid='$jkpromoid',prepos='$jkprepos',ARBflag='$jkARBflag' where mobno='$mobno'");
								$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$jktuneno','$jktunety','$jkdate','$jkexpdate','$jksdate','$jkplaydate','$jkactivate',1,'$jkuserstatus','$jksubtype','$jksubtyname','$jksid','$jkRenewalFlag','$jkfreetune','$jkpromoid','$jkprepos','$jkARBflag')");
						}

							$maxsno=$maxsno-1;
							$mysql->do("update jukebox set TuneSN=TuneSN-1 where TuneSN>'$TuneSN' and mobno='$mobno'");
							$mysql->do("insert into jukeboxmis(mobno,tunenumber,tunetype,date,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid) values ('$mobno','$juketuneno','$juketunety',now(),2,'$TuneSN','$jukeuserstatus','$subcriptiontype','$subtypename','$sid')");

							$mysql->disconnect();

							goto update;
						}

						&OtherFeatures;

					update:
						$dsql=DBI->connect($dsnd,$dbuser,$dbpasswd);
						$dsql->do("update MANSMSOBDpromobase_20Jan2015 set date=now(),activate=2,response='N' where mobno='$mobno'");
						$dsql->disconnect();

						$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
						$mysql->do("insert into deactivated (mobno,lang,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno','$lang',now(),2,'$subcriptiontype','$subtypename','$sid')");
						$mysql->disconnect();

						#$message="Ur FREE TUNE is now deactivated free of charge. For more hellotunes call 369.";

						$MsgID="1080";
						&SendConfSMS;

						exit;
					}
					else
					{
						#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

						$MsgID="1082";
						&SendConfSMS;

						exit;
					}
				}
				elsif($status==4)
				{
					#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

					$MsgID="1082";
					&SendConfSMS;

					exit;
				}
			}
			elsif($message eq "Y")
			{
				#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";

				$MsgID="1082";
				&SendConfSMS;

				exit;
			}
		}
		elsif($activate==2)
		{
			#$message="Your Free Tune is already deactivated! Thank you. Hutch";

			$MsgID="1081";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Dear Customer, you do not have any free Tune. To activate hellotunes call to 369.";
		
		$MsgID="1082";
		&SendConfSMS;

		exit;
	}

################################################ HT N Non User Promotion -- End ##################################################

}


sub OtherFeatures
{
##################################### Finding Active tunes from ALL features -- Start #######################################

	$flag=0;

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

	@features=(spgroup,spcaller,sptime,tunepack,gift);

	foreach $table (@features)
	{
		$flag=0;

		if($table eq "spgroup")
		{
			$str=$mysql->prepare("select assignto,groupnumber,tunenumber,tunetype,date,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos from spgroup where mobno='$mobno' and mobno=assignto and groupnumber>0 and playdate + INTERVAL 7 DAY > curdate() and activate=1 order by date desc limit 1");
			$str->execute;
			@spgroup=$str->fetchrow();
			$spgrows=$str->rows;
			$str->finish();

			$spgassignto=$spgroup[0];
			$spggrpnumber=$spgroup[1];
			$spgtunenumber=$spgroup[2];
			$spgtunetype=$spgroup[3];
			$spgdate=$spgroup[4];
			$spgexpdate=$spgroup[5];
			$spgactivate=$spgroup[6];
			$spguserstatus=$spgroup[7];
			$spgsubtype=$spgroup[8];
			$spgsubtypename=$spgroup[9];
			$spgserverid=$spgroup[10];
			$spgRenewalFlag=$spgroup[11];
			$spfreetune=$spgroup[12];
			$sppromoid=$spgroup[13];
			$spprepos=$spgroup[14];

			if($spgrows>0)
			{
				$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunetype='$spgtunetype' and tunenumber='$spgtunenumber'");
				$str->execute;
				$MTRcomment=$str->fetchrow();
				$str->finish();

				$MTRcomment="$MTRcomment : CLI $mobno";

				$mysql->do("update existnewsubscriber set assignto='$spgassignto',groupnumber='$spggrpnumber',tunenumber='$spgtunenumber',tunetype='$spgtunetype',date='$spgdate',expdate='$spgexpdate',activate='$spgactivate',subcriptiontype='$spgsubtype',subtypename='$spgsubtypename',serverid='$spgserverid',userstatus='$spguserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',freetune='$spfreetune',promoid='$sppromoid',prepos='$spprepos' where mobno='$mobno'");

				$flag=1;
				last;
			}
			else
			{
				next;
			}
		}
		elsif($table eq "spcaller")
		{
			$str=$mysql->prepare("select assignto,tunenumber,tunetype,date,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos from spcaller where mobno='$mobno' and mobno<>assignto and groupnumber=0 and playdate + INTERVAL 7 DAY > curdate() and activate=1 order by date desc limit 1");
			$str->execute;
			@spcaller=$str->fetchrow();
			$spcrows=$str->rows;
			$str->finish();

			$spcassignto=$spcaller[0];
			$spctunenumber=$spcaller[1];
			$spctunetype=$spcaller[2];
			$spcdate=$spcaller[3];
			$spcexpdate=$spcaller[4];
			$spcactivate=$spcaller[5];
			$spcuserstatus=$spcaller[6];
			$spcsubtype=$spcaller[7];
			$spcsubtypename=$spcaller[8];
			$spcserverid=$spcaller[9];
			$spcRenewalFlag=$spcaller[10];
			$spcfreetune=$spcaller[11];
			$spcpromoid=$spcaller[12];
			$spcprepos=$spcaller[13];

			if($spcrows>0)
			{
				$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunetype='$spctunetype' and tunenumber='$spctunenumber'");
				$str->execute;
				$MTRcomment=$str->fetchrow();
				$str->finish();

				$MTRcomment="$MTRcomment : CLI $spcassignto";

				$mysql->do("update existnewsubscriber set assignto='$spcassignto',tunenumber='$spctunenumber',tunetype='$spctunetype',date='$spcdate',expdate='$spcexpdate',activate='$spcactivate',subcriptiontype='$spcsubtype',subtypename='$spcsubtypename',serverid='$spcserverid',userstatus='$spcuserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',freetune='$spcfreetune',promoid='$spcpromoid',prepos='$spcprepos' where mobno='$mobno'");

				$flag=1;
				last;
			}
			else
			{
				next;
			}
		}
		elsif($table eq "sptime")
		{
			$str=$mysql->prepare("select tunenumber,tunetype,date,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos from sptime where mobno='$mobno' and playdate + INTERVAL 7 DAY > curdate() and activate=1 order by date desc limit 1");
			$str->execute;
			@sptime=$str->fetchrow();
			$sptrows=$str->rows;
			$str->finish();

			$spttunenumber=$sptime[0];
			$spttunetype=$sptime[1];
			$sptdate=$sptime[2];
			$sptexpdate=$sptime[3];
			$sptactivate=$sptime[4];
			$sptuserstatus=$sptime[5];
			$sptsubtype=$sptime[6];
			$sptsubtypename=$sptime[7];
			$sptserverid=$sptime[8];
			$sptRenewalFlag=$sptime[9];
			$sptfreetune=$sptime[10];
			$sptpromoid=$sptime[11];
			$sptprepos=$sptime[12];

			if($sptrows>0)
			{
				$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunetype='$spttunetype' and tunenumber='$spttunenumber'");
				$str->execute;
				$MTRcomment=$str->fetchrow();
				$str->finish();

				$mysql->do("update existnewsubscriber set tunenumber='$spttunenumber',tunetype='$spttunetype',date='$sptdate',expdate='$sptexpdate',activate='$sptactivate',subcriptiontype='$sptsubtype',subtypename='$sptsubtypename',serverid='$sptserverid',userstatus='$sptuserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',freetune='$sptfreetune',promoid='$sptpromoid',prepos='$sptprepos' where mobno='$mobno'");

				$flag=1;
				last;
			}
			else
			{
				next;
			}
		}
		elsif($table eq "tunepack")
		{
			$str=$mysql->prepare("select p.tpnumber,p.tptype,t.date,t.playdate,t.activate,t.userstatus,t.subcriptiontype,t.subtypename,t.serverid,t.RenewalFlag,p.contprov,t.freetune,t.promoid,t.prepos from tunepack t,tunepacktunes p where t.mobno='$mobno' and t.TuneSN=p.tpnumber and t.tunenumber=p.tunenumber and t.tunetype=p.tunetype and t.playdate + INTERVAL 7 DAY > curdate() and t.activate=1 order by t.date desc limit 1");
			$str->execute;
			@tunepack=$str->fetchrow();
			$tprows=$str->rows;
			$str->finish();

			$tptunenumber=$tunepack[0];
			$tptunetype=$tunepack[1];
			$tpdate=$tunepack[2];
			$tpexpdate=$tunepack[3];
			$tpactivate=$tunepack[4];
			$tpuserstatus=$tunepack[5];
			$tpsubtype=$tunepack[6];
			$tpsubtypename=$tunepack[7];
			$tpserverid=$tunepack[8];
			$tpRenewalFlag=$tunepack[9];
			$tcp=$tunepack[10];
			$tpfreetune=$tunepack[11];
			$tppromoid=$tunepack[12];
			$tpprepos=$tunepack[13];

			if($tprows>0)
			{
				$MTRcomment="CRBT SN $tptunenumber M P $tcp";

				$mysql->do("update existnewsubscriber set tunenumber='$tptunenumber',tunetype='$tptunetype',date='$tpdate',expdate='$tpexpdate',activate='$tptactivate',subcriptiontype='$tpsubtype',subtypename='$tpsubtypename',serverid='$tpserverid',userstatus='$tpuserstatus',billed=1,HTservice=1,MTRcomment='$MTRcomment',freetune='$tpfreetune',promoid='$tppromoid',prepos='$tpprepos' where mobno='$mobno'");

				$flag=1;
				last;
			}
			else
			{
				next;
			}
		}
		elsif($table eq "gift")
		{
			$str=$mysql->prepare("select assignto,tunenumber,tunetype,date,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos from gift where activate=1 and mobno='$mobno' order by date desc limit 1");
			$str->execute;
			@gifttune=$str->fetchrow();
			$gtrows=$str->rows;
			$str->finish();

			$gtassignto=$gifttune[0];
			$gttunenumber=$gifttune[1];
			$gttunetype=$gifttune[2];
			$gtdate=$gifttune[3];
			$gtexpdate=$gifttune[4];
			$gtactivate=$gifttune[5];
			$gtuserstatus=$gifttune[6];
			$gtsubtype=$gifttune[7];
			$gtsubtypename=$gifttune[8];
			$gtserverid=$gifttune[9];
			$gtRenewalFlag=$gifttune[10];
			$gtfreetune=$gifttune[11];
			$gtpromoid=$gifttune[12];
			$gtprepos=$gifttune[13];

			if($gtrows>0)
			{
				$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunetype='$gttunetype' and tunenumber='$gttunenumber'");
				$str->execute;
				$MTRcomment=$str->fetchrow();
				$str->finish();

				$MTRcomment="$MTRcomment : GIFT $gtassignto";

				$mysql->do("update existnewsubscriber set assignto='$gtassignto',tunenumber='$gttunenumber',tunetype='$gttunetype',date='$gtdate',expdate='$gtexpdate',activate='$gtactivate',subcriptiontype='$gtsubtype',subtypename='$gtsubtypename',serverid='$gtserverid',userstatus='$gtuserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',freetune='$gtfreetune',promoid='$gtpromoid',prepos='$gtprepos' where mobno='$mobno'");

				$flag=1;
				last;
			}
			else
			{
				next;
			}
		}
	}

	if($flag==0)
	{
		$mysql->do("update existnewsubscriber set date=now(),activate=2,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',HTservice=2,freetune=0,promoid=0,prepos='$prepos' where mobno='$mobno'");
		$mysql->do("insert into existnewsubscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid,HTservice,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid',2,'$prepos')");
	}

	$mysql->disconnect();

###################################### Finding Active tunes from ALL features -- End ########################################

}


sub GETTUNEID
{
	$sid="1";
	$subcriptiontype="8";
	$subtypename="SMS";
	$freetune="0";
	$promoid="0";
	$fbillamt="0";
	$balance="0";
	$RenewalFlag="0";
	$ARBflag="0";

	############################################### Check TRYnBUY Offer ###############################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from TRYnBUYOffer where mobno='$mobno' and topick=0 and activate=0 and DATEDIFF(curdate(),date(insdate)) in(0,1,2,3,4) and prepos=0");
	$str->execute;
	$trycount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($trycount)
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$str=$mysql->prepare("select tunelist from TRYnBUYOffer where mobno='$mobno' and topick=0 and activate=0 and DATEDIFF(curdate(),date(insdate)) in(0,1,2,3,4) and prepos=0");
		$str->execute;
		@tunelist=$str->fetchrow();
		$str->finish();

		$str=$mysql->prepare("select sno from TRYnBUYOffer where mobno='$mobno' and topick=0 and activate=0 and DATEDIFF(curdate(),date(insdate)) in(0,1,2,3,4) and prepos=0");
		$str->execute;
		$tsno=$str->fetchrow();
		$str->finish();

		$mysql->disconnect();

		if(grep {$_ eq $tuneid} @tunelist) #check the tune with tunelist
		{
			&TRYnBUYPromotion;
			exit;
		}
		else
		{
			# Go for normal activation if customer send another tune(not in given tunelist)
		}
	}

	############################################### Check TRYnBUY Offer ###############################################


	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),lang,activate,subscridate from existnewsubscriber where mobno='$mobno' group by mobno");
	$str->execute;
	@nesubs=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$necnt=$nesubs[0];
	$lang=$nesubs[1];
	$activate=$nesubs[2];
	$subscridate=$nesubs[3];

	if($necnt==0)
	{
		$lang=3;
		$userstatus='N';
	}
	elsif($necnt==1)
	{
		if($activate==1) 
		{
			$userstatus='E';
		}
		elsif($activate==2) 
		{
			$lang=3;
			$userstatus='N';
		}
	}

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1025";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to activate the requested Hello Tune as you are Pre activated with a Corporate tune. When this expires you will be enabled for normal activation.";

		$MsgID="1020";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select tunenumber,tunetype,concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tuneid='$tuneid' and ivrno<>0 and IsValid=1");
	$str->execute;
	@tunearr=$str->fetchrow();
	$tunecnt=$str->rows;
	$str->finish();
	$mysql->disconnect();

	$tunenumber=$tunearr[0];
	$tunetype=$tunearr[1];
	$MTRcomment=$tunearr[2];

	if($tunecnt==0)
	{
		#$message="The tune ID you sent is incorrect. Please send correct Tune ID.";

		$MsgID="1017";
		&SendConfSMS;

		exit;
	}
	elsif($tunecnt>0)
	{
	########################################### Checking for Existance of Same Tune ########################################### 

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$str=$mysql->prepare("select count(*) from subscriber where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1");
		$str->execute;
		$subscnt=$str->fetchrow();
		$str->finish();

		$str=$mysql->prepare("select count(*) from jukebox where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1");
		$str->execute;
		$jukecnt=$str->fetchrow();
		$str->finish();

		$mysql->disconnect();

		if($subscnt==0 && $jukecnt==0)
		{}
		elsif($subscnt==1 || $jukecnt==1)
		{
			#$message="Dear Customer, you are already active with the requested tune. Please try again with another tune. Thank you.";

			$MsgID="1018";
			&SendConfSMS;

			exit;
		}


	########################################### Checking for Existance of Same Tune ########################################### 

	#################################### Charges and Expdates Calculation -- Start ######################################

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$str=$mysql->prepare("select preamt,postamt,tax from charges");
		$str->execute;
		@charges=$str->fetchrow();
		$str->finish();

		$preamt=$charges[0];
		$postamt=$charges[1];
		$tax=$charges[2];

		$tax=($tax/100);

		$str=$mysql->prepare("select (CASE 1 WHEN DAY(curdate())<18 THEN DATE_FORMAT(curdate(),'%Y-%m-18') WHEN DAY(curdate())>=18 THEN DATE_FORMAT(curdate() + INTERVAL 1 MONTH,'%Y-%m-18') ELSE '' END) as ExpDate,(select round((('$postamt'/30) * '$tax' + ('$postamt'/30))*(CASE 1 WHEN DAY(curdate())<18 THEN DATEDIFF(DATE_FORMAT(curdate(),'%Y-%m-18'),curdate()) WHEN DAY(curdate())>=18 THEN DATEDIFF(DATE_FORMAT(curdate() + INTERVAL 1 MONTH,'%Y-%m-18'),curdate()) ELSE '' END),2))");
		$str->execute;
		@postpaid=$str->fetchrow();
		$str->finish();

		$postexpdate=$postpaid[0];
		$postamount=$postpaid[1];

		$str=$mysql->prepare("select curdate() + INTERVAL 30 DAY,curdate() + INTERVAL 90 DAY,round((($preamt/30) * $tax + ($preamt/30))*30,2)");
		$str->execute;
		@prnpr=$str->fetchrow();
		$str->finish();

		$prexpdate=$prnpr[0];
		$nprexpdate=$prnpr[1];
		$prnpramt=$prnpr[2];

		$mysql->disconnect();

	##################################### Charges and Expdates Calculation -- End #######################################

		if($prepos==1)
		{
			$expdate=$postexpdate;
			$amount=$postamount;
		}
		elsif($prepos==0)
		{
			if(substr($tunetype,0,2) eq "PR")
			{
				$expdate=$prexpdate;
				$amount=$prnpramt;
			}
			elsif(substr($tunetype,0,2) eq "NP")
			{
				$expdate=$nprexpdate;
				$amount=$prnpramt;
			}

			&MicroCharging;
		}

		if($skipbilling==1)
		{
			$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
			$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,status,fbillamt,balance,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',1,'$retval','$fbillamt','$balance','$amount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$prepos')");
			$bsql->disconnect();

			$skipbilling=0;
		}
		else
		{
			$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
			$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,fbillamt,balance,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',1,'$fbillamt','$balance','$amount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$prepos')");
			$bsql->disconnect();

			$agent=LWP::UserAgent->new;
			$request=POST "http://192.168.100.28/inbilling/WebForm1.aspx?msisdn=$mobno&amount=$amount&tunetype=$tunetype&tunenumber=$tunenumber&billsrc=2&CP=$MTRcomment&subtype=$subcriptiontype&subtypename=$subtypename";
			$response=$agent->request($request);
			$rep=$response->as_string;
			@extract=split('\\n',$rep);
			$retval=$extract[$#extract];

			$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
			$bsql->do("update billing set date=now(),status='$retval' where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and status=0 and date(date)=curdate() and amount='$amount' order by date desc limit 1");
			$bsql->disconnect();
		}

		if($necnt==0)
		{
			$subscridate=`date "+%F %T"`;
			chomp($subscridate);
		}
		elsif($necnt==1)
		{
			if($userstatus eq "N")
			{
				$subscridate=`date "+%F %T"`;
				chomp($subscridate);
			}
		}

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$mysql->do("insert into existnewsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,fbillamt,balance,amount,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$expdate',1,'$subscridate','$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$fbillamt','$balance','$amount',1,'$MTRcomment','$freetune','$promoid','$prepos')");
		$mysql->disconnect();

		if($retval==1)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			if($necnt==0)
			{
				$mysql->do("insert into existnewsubscriber (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$expdate',1,now(),'$subcriptiontype','$subtypename','$sid','$userstatus','$retval',1,'$MTRcomment','$freetune','$promoid','$prepos')");
			}
			elsif($necnt==1)
			{
				if($userstatus eq "N")
				{
					$mysql->do("update existnewsubscriber set assignto=0,lang='$lang',tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',activate=1,subscridate=now(),subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',billed='$retval',HTservice=1,MTRcomment='$MTRcomment',freetune='$freetune',promoid='$promoid',prepos='$prepos'  where mobno='$mobno'");
				}
				elsif($userstatus eq "E")
				{
					$mysql->do("update existnewsubscriber set assignto=0,lang='$lang',tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',activate=1,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',billed='$retval',HTservice=1,MTRcomment='$MTRcomment',freetune='$freetune',promoid='$promoid',prepos='$prepos' where mobno='$mobno'");
				}
			}

			$str=$mysql->prepare("select count(*),tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag from subscriber where mobno='$mobno' group by mobno");
			$str->execute;
			@subs=$str->fetchrow();
			$str->finish();

			$subscnt=$subs[0];
			$stunenumber=$subs[1];
			$stunetype=$subs[2];
			$sdate=$subs[3];
			$sexpdate=$subs[4];
			$ssdate=$subs[5];
			$splaydate=$subs[6];
			$sactivate=$subs[7];
			$JKflag=$subs[8];
			$suserstatus=$subs[9];
			$ssubtype=$subs[10];
			$ssubtypename=$subs[11];
			$sserverid=$subs[12];
			$sRenewalFlag=$subs[13];
			$sfreetune=$subs[14];
			$spromoid=$subs[15];
			$sprepos=$subs[16];
			$sARBflag=$subs[17];

			$str=$mysql->prepare("select count(*),max(TuneSN) from jukebox where activate=1 and mobno='$mobno' group by mobno");
			$str->execute;
			@juke=$str->fetchrow();
			$str->finish();

			$mysql->disconnect();

			$jukecnt=$juke[0];
			$maxsno=$juke[1];

			if($subscnt==0)
			{
				$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

				$mysql->do("insert into subscriber (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,'$userstatus','$subcriptiontype','$subtypename','$sid','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");
				$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,userstatus,subcriptiontype,subtypename,serverid,billed,amount,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,'$userstatus','$subcriptiontype','$subtypename','$sid','$retval','$amount','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");

				$mysql->disconnect();
			}
			elsif($subscnt==1)
			{
				if($JKflag==0)
				{
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$mysql->do("update subscriber set JKflag=1 where mobno='$mobno'");
					$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,prepos) values ('$mobno','$stunenumber','$stunetype',now(),'$sactivate',1,'$suserstatus','$subcriptiontype','$subtypename','$sid','$sprepos')");
					$mysql->do("delete from jukebox where tunenumber='$stunenumber' and tunetype='$stunetype' and deftune=1 and mobno='$mobno'");
					$mysql->do("update jukebox set deftune=0 where mobno='$mobno'");

					$nextsno=$maxsno+1;
					$mysql->do("insert into jukebox (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,deftune,TuneSN,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$stunenumber','$stunetype','$sdate','$sexpdate','$ssdate','$splaydate','$sactivate',1,'$nextsno','$suserstatus','$ssubtype','$ssubtypename','$sserverid','$sRenewalFlag','$sfreetune','$spromoid','$sprepos','$sARBflag')");
					$mysql->do("insert into jukeboxmis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,deftune,TuneSN,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$stunenumber','$stunetype','$sdate','$sexpdate','$ssdate','$splaydate','$sactivate',1,'$nextsno','$suserstatus','$ssubtype','$ssubtypename','$sserverid','$sRenewalFlag','$sfreetune','$spromoid','$sprepos','$sARBflag')");

					$nextsno=$maxsno+2;
					$mysql->do("insert into jukebox (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,'$nextsno','$userstatus','$subcriptiontype','$subtypename','$sid','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");
					$mysql->do("insert into jukeboxmis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid,billed,amount,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,'$nextsno','$userstatus','$subcriptiontype','$subtypename','$sid','$retval','$amount','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");

					$mysql->disconnect();
				}
				elsif($JKflag==1)
				{
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$nextsno=$maxsno+1;
					$mysql->do("insert into jukebox (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,'$nextsno','$userstatus','$subcriptiontype','$subtypename','$sid','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");
					$mysql->do("insert into jukeboxmis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,TuneSN,userstatus,subcriptiontype,subtypename,serverid,billed,amount,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,'$nextsno','$userstatus','$subcriptiontype','$subtypename','$sid','$retval','$amount','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");

					$mysql->disconnect();
				}
			}

			if($microsms==1)
			{
				$microsms="0";
				#$message= "You will be charged with Rs.$billeddays %2B Tax %26 a daily fee of Rs.1.50. The tune is valid for $nobdays days.";

				$MsgID="1016";
				&SendConfSMS;

				exit;
			}
			else
			{
				$Response=substr($tunetype,0,2);

				if($Response eq "PR")
				{
					if($prepos==0)
					{
						#$message="Thank you for using Premium Tunes. You will be charged a tune subscription of Rs.30 %2B Tax %26 a daily fee of Rs.1.50. The tune is valid for 30 days.";

						$MsgID="1012";
					}
					elsif($prepos==1)
					{
						#$message="Thank you for using Hello Tunes. You will be charged a tune subscription of Rs.40 %2B Tax. The tune is valid for 30 days.";

						$MsgID="1013";
					}
				}
				elsif($Response eq "NP")
				{
					if($prepos==0)
					{
						#$message="Thank you for using Non Premium Tunes. You will be charged a tune subscription of Rs.30 %2B Tax %26 a daily fee of Rs.1.50. The tune is valid for 90 days.";

						$MsgID="1014";
					}
					elsif($prepos==1)
					{
						#$message="Thank you for using Hello Tunes. U will be charged with a tune subscription of Rs.40 %2B Tax. The tune is valid for 30 days.";

						$MsgID="1015";
					}
				}

				&SendConfSMS;

				exit;
			}
		}
		elsif($retval==4)
		{
			#$message="Your tune request has failed due to low balance. Recharge your account and try again. Thank you.";

			$MsgID="1019";
			&SendConfSMS;

			exit;
		}
		else
		{
			#$message="Your tune request has failed. Please try again later. Thank you.";

			$MsgID="1023";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1025";
		&SendConfSMS;

		exit;
	}
}


sub TRYnBUYPromotion
{
	$freetune="1";
	$promoid="200";
	$RenewalFlag="0";
	$ARBflag="0";

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),lang,activate,subscridate from existnewsubscriber where mobno='$mobno' group by mobno");
	$str->execute;
	@nesubs=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$necnt=$nesubs[0];
	$lang=$nesubs[1];
	$activate=$nesubs[2];
	$subscridate=$nesubs[3];

	if($necnt==0)
	{
		$lang=3;
		$userstatus='N';
	}
	elsif($necnt==1)
	{
		if($activate==1) 
		{
			$userstatus='E';
		}
		elsif($activate==2) 
		{
			$lang=3;
			$userstatus='N';
		}
	}

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1025";
		&SendConfSMS;

		exit;
	}

	if($necnt==1)
	{
		if($activate==1) 
		{
			$userstatus='E';

			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
			$mysql->do("update TRYnBUYOffer set date=now(),topick=3,activate=3,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',prepos='$prepos' where sno='$tsno'");
			$mysql->disconnect();

			#$message="Dear Customer, you are already active with Hello Tune service. Thank you. Hutch";

			$MsgID="1254";
			&SendConfSMS;

			exit;

		}
	}

################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to activate the requested Hello Tune as you are Pre activated with a Corporate tune. When this expires you will be enabled for normal activation.";

		$MsgID="1020";
		&SendConfSMS;

		exit;
	}

################################################# CHECK CORPORATE TUNE #################################################
        
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select tunenumber,tunetype,concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tuneid='$tuneid' and ivrno<>0 and IsValid=1");
	$str->execute;
	@tunearr=$str->fetchrow();
	$tunecnt=$str->rows;
	$str->finish();
	$mysql->disconnect();

	$tunenumber=$tunearr[0];
	$tunetype=$tunearr[1];
	$MTRcomment=$tunearr[2];

	if($tunecnt==0)
	{
		#$message="The tune ID you sent is incorrect. Please send correct Tune ID.";

		$MsgID="1017";
		&SendConfSMS;

		exit;
	}
	elsif($tunecnt>0)
	{
########################################### Checking for Existance of Same Tune ########################################### 

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$str=$mysql->prepare("select count(*) from subscriber where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and activate=1");
		$str->execute;
		$subscnt=$str->fetchrow();
		$str->finish();
		$mysql->disconnect();

		if($subscnt==0)
		{}
		elsif($subscnt==1)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
			$mysql->do("update TRYnBUYOffer set date=now(),topick=3,activate=3,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus' where sno='$tsno'");
			$mysql->disconnect();

			#$message="Dear Customer, you are already active with the requested tune. Please try again with another tune. Thank you.";

			$MsgID="1018";
			&SendConfSMS;

			exit;
		}


########################################### Checking for Existance of Same Tune ########################################### 

		$amount=0;

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$str=$mysql->prepare("select curdate() + INTERVAL 5 DAY");
		$str->execute;
		$expdate=$str->fetchrow();
		$str->finish();
		$mysql->disconnect();

		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,prepos,freetune,promoid) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',1,'$amount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$prepos','$freetune','$promoid')");
		$bsql->disconnect();

		$agent=LWP::UserAgent->new;
		$request=POST "http://192.168.100.28/inbilling/WebForm1.aspx?msisdn=$mobno&amount=$amount&tunetype=$tunetype&tunenumber=$tunenumber&billsrc=2&CP=$MTRcomment&subtype=$subcriptiontype&subtypename=$subtypename";
		$response=$agent->request($request);
		$rep=$response->as_string;
		@extract=split('\\n',$rep);
		$retval=$extract[$#extract];

		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("update billing set date=now(),status='$retval' where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and status=0 and date(date)=curdate() and amount='$amount' order by date desc limit 1");
		$bsql->disconnect();

		if($necnt==0)
		{
			$subscridate=`date "+%F %T"`;
			chomp($subscridate);
		}
		elsif($necnt==1)
		{
			if($userstatus eq "N")
			{
				$subscridate=`date "+%F %T"`;
				chomp($subscridate);
			}
		}

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$mysql->do("insert into existnewsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,amount,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$expdate',1,'$subscridate','$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$amount',1,'$MTRcomment','$freetune','$promoid','$prepos')");
		$mysql->disconnect();

		if($retval==1)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			if($necnt==0)
			{
				$mysql->do("insert into existnewsubscriber (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$expdate',1,now(),'$subcriptiontype','$subtypename','$sid','$userstatus','$retval',1,'$MTRcomment','$freetune','$promoid','$prepos')");
			}
			elsif($necnt==1)
			{
				if($userstatus eq "N")
				{
					$mysql->do("update existnewsubscriber set assignto=0,lang='$lang',tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',activate=1,subscridate=now(),subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',billed='$retval',HTservice=1,MTRcomment='$MTRcomment',freetune='$freetune',promoid='$promoid',prepos='$prepos'  where mobno='$mobno'");
				}
				elsif($userstatus eq "E")
				{
					$mysql->do("update existnewsubscriber set assignto=0,lang='$lang',tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',activate=1,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',billed='$retval',HTservice=1,MTRcomment='$MTRcomment',freetune='$freetune',promoid='$promoid',prepos='$prepos' where mobno='$mobno'");
				}
			}

			$str=$mysql->prepare("select count(*) from subscriber where mobno='$mobno'");
			$str->execute;
			$subscnt=$str->fetchrow();
			$str->finish();

			$mysql->disconnect();

			if($subscnt==0)
			{
				$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

				$mysql->do("insert into subscriber (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,0,'$userstatus','$subcriptiontype','$subtypename','$sid','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");
				$mysql->do("insert into subscribermis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,JKflag,userstatus,subcriptiontype,subtypename,serverid,billed,amount,RenewalFlag,freetune,promoid,prepos,ARBflag) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,0,'$userstatus','$subcriptiontype','$subtypename','$sid','$retval','$amount','$RenewalFlag','$freetune','$promoid','$prepos','$ARBflag')");

				$mysql->do("update TRYnBUYOffer set date=now(),expdate='$expdate',tunenumber='$tunenumber',tunetype='$tunetype',topick=1,activate=1,response='YES',subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus' where sno='$tsno'");

				$mysql->disconnect();
			}

			#$message="U have successfully activated a FREE Hello Tune valid for 5 days. Kindly note the tune will auto renew thereafter. Rs.30 %2BTax will be charged on auto renewal.";

			$MsgID="1021";
			&SendConfSMS;

			exit;
		}
		elsif($retval==4)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
			$mysql->do("update TRYnBUYOffer set date=now(),expdate='$expdate',topick=4,activate=4,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus' where sno='$tsno'");
			$mysql->disconnect();

			#$message="Your tune request has failed due to low balance. Recharge your account and try again. Thank you.";

			$MsgID="1019";
			&SendConfSMS;

			exit;
		}
		else
		{
			#$message="Your tune request has failed. Please try again later. Thank you.";

			$MsgID="1023";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1025";
		&SendConfSMS;

		exit;
	}
}


sub GIFTDA
{
	$mobno=substr($mobno,-9,9);
	$assignto=substr($assignto,-9,9);

	$sid=1;
	$subcriptiontype="8";
	$subtypename="SMS";
	$RenewalFlag="0";
	$ARBflag="0";

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1036";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to deactivate your GiftTune, since you are Pre activated with Corprate tune.Thank you. Hutch";

		$MsgID="1035";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),sno,activate,tunenumber,tunetype,prepos from gift where mobno='$mobno' and assignto='$assignto' group by mobno");
	$str->execute;
	@gift=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$giftcnt=$gift[0];
	$sno=$gift[1];
	$activate=$gift[2];
	$tunenumber=$gift[3];
	$tunetype=$gift[4];
	$gprepos=$gift[5];

	if($giftcnt==0)
	{
		#$message="Dear Customer, You have not Gifted any tune to the number $assignto. Thank You.";
		$userstatus='E';

		$MsgID="1032";
		&SendConfSMS;

		exit;
	}
	elsif($giftcnt==1)
	{
		if($activate==1)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			$mysql->do("insert into deactivated (mobno,lang,assignto,tunenumber,tunetype,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno','$lang','$assignto','$tunenumber','$tunetype',now(),2,'$subcriptiontype','$subtypename','$sid','$gprepos')");

			$mysql->do("update gift set date=now(),activate=2,tobill=0,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',RenewalFlag='$RenewalFlag',ARBflag='$ARBflag' where sno='$sno'");
			$mysql->do("insert into giftmis (mobno,assignto,tunenumber,tunetype,date,activate,userstatus,subcriptiontype,subtypename,serverid,prepos)  values ('$mobno','$assignto','$tunenumber','$tunetype',now(),2,'E','$subcriptiontype','$subtypename','$sid','$gprepos')");

			$str=$mysql->prepare("select count(*),activate,HTservice from existnewsubscriber where mobno='$mobno' group by mobno");
			$str->execute;
			@nesubs=$str->fetchrow();
			$str->finish();

			$mysql->disconnect();

			$nesubscnt=$nesubs[0];
			$neactivate=$nesubs[1];
			$HTservice=$nesubs[2];

			if($nesubscnt==1)
			{
				if($neactivate==1 && $HTservice==2)
				{
					$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

					$str=$mysql->prepare("select assignto,tunenumber,tunetype,date,expdate,activate,userstatus,subcriptiontype,subtypename,serverid,RenewalFlag,prepos from gift where activate=1 and mobno='$mobno' order by date desc limit 1");
					$str->execute;
					@gifttune=$str->fetchrow();
					$gtrows=$str->rows;
					$str->finish();

					$gtassignto=$gifttune[0];
					$gttunenumber=$gifttune[1];
					$gttunetype=$gifttune[2];
					$gtdate=$gifttune[3];
					$gtexpdate=$gifttune[4];
					$gtactivate=$gifttune[5];
					$gtuserstatus=$gifttune[6];
					$gtsubtype=$gifttune[7];
					$gtsubtypename=$gifttune[8];
					$gtserverid=$gifttune[9];
					$gtRenewalFlag=$gifttune[10];
					$gtprepos=$gifttune[11];

					if($gtrows==0)
					{
						$mysql->do("update existnewsubscriber set date=now(),activate=2,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid' where mobno='$mobno'");
						$mysql->do("insert into existnewsubscribermis(mobno,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");
					}
					elsif($gtrows>0)
					{
						$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunenumber='$gttunenumber' and tunetype='$gttunetype'");
						$str->execute;
						$MTRcomment=$str->fetchrow();
						$str->finish();
						$mysql->disconnect();

						$MTRcomment="$MTRcomment : GIFT $gtassignto";

						$mysql->do("update existnewsubscriber set assignto='$gtassignto',tunenumber='$gttunenumber',tunetype='$gttunetype',date='$gtdate',expdate='$gtexpdate',activate='$gtactivate',subcriptiontype='$gtsubtype',subtypename='$gtsubtypename',serverid='$gtserverid',userstatus='$gtuserstatus',billed=1,HTservice=2,MTRcomment='$MTRcomment',prepos='$gtprepos' where mobno='$mobno'");
						$mysql->do("insert into existnewsubscribermis (mobno,assignto,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,HTservice,MTRcomment,prepos) values('$mobno','$gtassignto','$gttunenumber','$gttunetype','$gtdate','$gtexpdate','$gtactivate','$gtsubtype','$gtsubtypename','$gtserverid','$gtuserstatus',1,2,'$MTRcomment','$gtprepos')");
					}

					$mysql->disconnect();
				}
				elsif($neactivate==2)
				{
					#$message="You are Already DeActivated, To Activate the Service please call 369. Charges Apply.";

					$userstatus='E';

					$MsgID="1034";
					&SendConfSMS;
					exit;
				}
			}

			#$message="You have successfully Deactivated Gift Hello tune Service. Thank you for using Hello Tunes. Good bye !";

			$userstatus='E';

			$MsgID="1033";
			&SendConfSMS;

			exit;
		}
		elsif($activate==2)
		{
			#$message="You are Already Deactivated, To Activate the Service please call 369. Charges Apply.";

			$userstatus='E';

			$MsgID="1034";
			&SendConfSMS;
		
			exit;
		}
	}
	else 
	{
		#$message="Server Busy, please try later.";
		$userstatus='E';

		$MsgID="1036";
		&SendConfSMS;

		exit;
	}
}


sub BTDA
{
	$mobno=substr($mobno,-9,9);

	$sid="1";
	$subcriptiontype="8";
	$subtypename="BUSY";
	$rcvmessage="BT DA";

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

	$str=$mysql->prepare("select count(*),activate,lang from BTsubscriber where mobno='$mobno'");
	$str->execute;
	@busytunes=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$busysubcount=$busytunes[0];
	$btactivate=$busytunes[1];
	$lang=$busytunes[2];

	if($busysubcount==0)
	{
		$lang="3";
		$userstatus='N';
	}
	elsif($busysubcount==1)
	{
		if($btactivate==1)
		{
			$userstatus='E';
		}
		elsif($btactivate==2)
		{
			$lang="3";
			$userstatus='N';
		}
	}

	$mysql->disconnect();

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$feature="BUSYTUNES";
		$MsgID="1258";
		&SendConfSMS;

		exit;
	}


	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to deactivate your Busy Tune service, since you are Pre activated with Corporate tune. Thank you. Hutch";

		$feature="BUSYTUNES";
		$MsgID="1257";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	if($busysubcount==0 || $btactivate==2)
	{
		#$message="You are Already Deactivated, To Activate the Busy Tunes please call 369. Charges Apply.";

		$feature="BUSYTUNES";
		$MsgID="1256";
		&SendConfSMS;

		exit;
	}
	else
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$str=$mysql->prepare("select tunenumber,tunetype from busytunes where mobno='$mobno'");
		$str->execute;
		@busytunes=$str->fetchrow();
		$str->finish();

		$tunenumber=$busytunes[0];
		$tunetype=$busytunes[1];

		$mysql->do("update BTsubscriber set date=now(),activate=2,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus' where mobno='$mobno'");

		$mysql->do("delete from busytunes where mobno='$mobno'");

		$mysql->do("insert into busytunesmis(mobno,tunenumber,tunetype,date,activate,subcriptiontype,subtypename,serverid,userstatus,prepos) values ('$mobno','$tunenumber','$tunetype',now(),2,'$subcriptiontype','$subtypename','$sid','$userstatus','$prepos')");

 		$mysql->do("insert into deactivated (mobno,lang,tunenumber,tunetype,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

		$mysql->disconnect();

		#$message="You have successfully deactivated Busy tune. Thank you for using Busy Tunes.";

		$feature="BUSYTUNES";
		$MsgID="1255";
		&SendConfSMS;

		exit;
	}
}


sub BTSUB
{
	$mobno=substr($mobno,-9,9);

	$sid="1";
	$subcriptiontype="8";
	$subtypename="BUSY";
	$freetune="0";
	$promoid="0";
	$rcvmessage="BT SUB";

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

	$str=$mysql->prepare("select count(*),(CASE 1 WHEN DATEDIFF(expdate,curdate()) is NULL THEN '0' ELSE DATEDIFF(expdate,curdate()) END),subscridate,activate,lang from BTsubscriber where mobno='$mobno'");
	$str->execute;
	@busyvalid=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$busysubcount=$busyvalid[0];
	$valid=$busyvalid[1];
	$subscridate=$busyvalid[2];
	$btactivate=$busyvalid[3];
	$lang=$busyvalid[4];

	if($busysubcount==0)
	{
		$lang="3";
		$userstatus='N';
	}
	elsif($busysubcount==1)
	{
		if($btactivate==1)
		{
			if($valid<=0)
			{
				$lang="3";
				$userstatus='N';
			}
			elsif($valid>0)
			{
				$userstatus='E';
				$amount=0;
			}
		}
		elsif($btactivate==2)
		{
			$lang="3";
			$userstatus='N';
		}
	}

	$mysql->disconnect();

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$feature="BUSYTUNES";
		$MsgID="1071";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to activate the requested BusyTune since u r Pre activated with Corporate tune. When this expires U will be enabled for normal activation.";

		$feature="BUSYTUNES";
		$MsgID="1070";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	if($valid>0 && $btactivate==1)
	{
		#$message="Dear customer u r already subscribed with Busy tunes. Thank you.";
	
		$feature="BUSYTUNES";
		$MsgID="1067";
		&SendConfSMS;

		exit;
	}
	elsif($valid<=0 || $btactivate==2) 
	{
		$amount="25.51";
		$tunenumber="100000";
		$tunetype="BUSY";

		$MTRcomment= "CRBT SN 100000 S B HUTCH";

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$str=$mysql->prepare("select curdate() + INTERVAL 30 DAY ");
		$str->execute;
		$btsexpdate=$str->fetchrow();
		$str->finish();
		$mysql->disconnect();

		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,freetune,promoid,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$btsexpdate',1,'$amount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$freetune','$promoid','$prepos')");
		$bsql->disconnect();

		$agent=LWP::UserAgent->new;
		$request=POST "http://192.168.100.28/inbilling/WebForm1.aspx?msisdn=$mobno&amount=$amount&tunetype=$tunetype&tunenumber=$tunenumber&billsrc=2&CP=$MTRcomment&subtype=$subcriptiontype&subtypename=$subtypename";
		$response=$agent->request($request);
		$rep=$response->as_string;
		@extract=split('\\n',$rep);
		$retval=$extract[$#extract];

		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("update billing set date=now(),status='$retval' where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and status=0 and date(date)=curdate() and amount='$amount' order by date desc limit 1");
		$bsql->disconnect();

		if($busysubcount==0)
		{
			$subscridate=`date "+%F %T"`;
			chomp($subscridate);
		}
		elsif($busysubcount==1)
		{
			if($userstatus eq "N")
			{
				$subscridate=`date "+%F %T"`;
				chomp($subscridate);
			}
		}

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$mysql->do("insert into existnewsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,amount,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$btsexpdate',1,'$subscridate','$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$amount',1,'$MTRcomment','$freetune','$promoid','$prepos')");
		$mysql->disconnect();

		##$retval=4;$lang=2;

		if($retval==1)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			if($busysubcount==0)
			{
				$mysql->do("insert into BTsubscriber (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$btsexpdate',1,now(),'$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$freetune','$promoid','$prepos')");
			}
			elsif($busysubcount==1)
			{
				$mysql->do("update BTsubscriber set lang='$lang',tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$btsexpdate',activate=1,subscridate=now(),subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',billed='$retval',freetune='$freetune',promoid='$promoid',prepos='$prepos' where mobno='$mobno'");
			}

			$mysql->do("insert into BTsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,amount,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$btsexpdate',1,now(),'$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$amount','$freetune','$promoid','$prepos')");

			$mysql->disconnect();

			#$message="Dear Customer, U have successfully subscribed for Busy tunes. You will be charged with a subscription of Rs. 20 %2B taxes valid for 30 days.";

			$feature="BUSYTUNES";
			$MsgID="1068";
			&SendConfSMS;

			exit;
		}
		elsif($retval>1)
		{
			#$message="Your subscription request has failed due to low balance. Please recharge your account and try again. Thank you.";

			$feature="BUSYTUNES";
			$MsgID="1069";
			&SendConfSMS;

			exit;
		}
	}
}



sub BTMESSAGE
{
	$mobno=substr($mobno,-9,9);

	$message = join(' ',split(' ',$message));
	$rcvmessage="BT "."$message";
	@array=split(' ',$message);
	@array=map { lc } @array;
	$argcnt=@array;

	$sid="1";
	$subcriptiontype="8";
	$subtypename="BUSY";

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),(CASE 1 WHEN DATEDIFF(expdate,curdate()) is NULL THEN '0' ELSE DATEDIFF(expdate,curdate()) END),subscridate,activate,lang from BTsubscriber where mobno='$mobno'");
	$str->execute;
	@busyvalid=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$busysubcount=$busyvalid[0];
	$valid=$busyvalid[1];
	$subscridate=$busyvalid[2];
	$btactivate=$busyvalid[3];
	$slang=$busyvalid[4];

	if($busysubcount==0)
	{
		$slang="3";
		$userstatus='N';
	}
	elsif($busysubcount==1)
	{
		if($btactivate==1)
		{
			if($valid<=0)
			{
				$slang="3";
				$userstatus='N';
			}
			elsif($valid>0)
			{
				$userstatus='E';
				$amount=0;
			}
		}
		elsif($btactivate==2)
		{
			$slang="3";
			$userstatus='N';
		}
	}

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$lang=$slang;
		$feature="BUSYTUNES";
		$MsgID="1066";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to activate the requested BusyTune since u r Pre activated with Corporate tune. When this expires U will be enabled for normal activation.";

		$lang=$slang;
		$feature="BUSYTUNES";
		$MsgID="1065";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	if($argcnt>4)
	{
		#$message="Send BT Meeting to activate Meeting Busy Tune for 1hr in English or BT Meeting T 3 to activate Meeting Busy Tune in Tamil for 3 hrs. Send BT to 369 for list of busy tunes.";

		$lang=$slang;
		$feature="BUSYTUNES";
		$MsgID="1047";
		&SendConfSMS;

		exit;
	}
	elsif($argcnt==4)
	{
		if($array[3] =~ m/[^0-9]/)
		{
			#$message="Send BT Meeting to activate Meeting Busy Tune for 1hr in English or BT Meeting T 3 to activate Meeting Busy Tune in Tamil for 3 hrs. Send BT to 369 for list of busy tunes.";

			$lang=$slang;
			$feature="BUSYTUNES";
			$MsgID="1047";
			&SendConfSMS;

			exit;
		}
		elsif($array[3] =~ m/[0-9]/)
		{
			@langs=('s','e','t','sinhala','english','tamil',0 .. 9);
			$match=0;
			foreach $lang (@langs)
			{
				if($array[1] eq $lang) { $match=1; last; }
			}

			if($match==1)
			{
				#$message="Send BT Meeting to activate Meeting Busy Tune for 1hr in English or BT Meeting T 3 to activate Meeting Busy Tune in Tamil for 3 hrs. Send BT to 369 for list of busy tunes.";

				$lang=$slang;
				$feature="BUSYTUNES";
				$MsgID="1047";
				&SendConfSMS;

				exit;
			}
			elsif($match==0)
			{
				$bttype = $array[0].' '.$array[1];

				@langs=('s','e','t','sinhala','english','tamil');
				$match=0;
				foreach $lang (@langs)
				{
					if($array[2] eq $lang) { $match=1; last; }
				}

				if($match==1) 
				{
					$btlang=$array[2];
					$bttime=$array[3];
				}
				else
				{
					#$message="Send BT Meeting to activate Meeting Busy Tune for 1hr in English or BT Meeting T 3 to activate Meeting Busy Tune in Tamil for 3 hrs. Send BT to 369 for list of busy tunes.";

					$lang=$slang;
					$feature="BUSYTUNES";
					$MsgID="1047";
					&SendConfSMS;

					exit;
				}
			}
		}
	}
	elsif($argcnt==3)
	{
		@langs=('s','e','t','sinhala','english','tamil');
		$match=0;
		foreach $lang (@langs)
		{
			if($array[1] eq $lang) { $match=1; last; }
		}

		if($match==1) 
		{
			if($array[2] =~ m/[^0-9]/)
			{
				#$message="Send BT Meeting to activate Meeting Busy Tune for 1hr in English or BT Meeting T 3 to activate Meeting Busy Tune in Tamil for 3 hrs. Send BT to 369 for list of busy tunes.";

				$lang=$slang;
				$feature="BUSYTUNES";
				$MsgID="1047";
				&SendConfSMS;

				exit;
			}
			elsif($array[2] =~ m/[0-9]/)
			{
				$bttype=$array[0];
				$btlang=$array[1];
				$bttime=$array[2];
			}
		}
		else
		{
			$bttype = $array[0].' '.$array[1];

			@langs=('s','e','t','sinhala','english','tamil');
			$match=0;
			foreach $lang (@langs)
			{
				if($array[2] eq $lang) { $match=1; last; }
			}

			if($match==1) 
			{
				$btlang=$array[2];
				$bttime="1";
			}
			elsif($array[2] =~ m/[0-9]/)
			{
				$btlang="e";
				$bttime=$array[2];
			}
			else
			{
				#$message="Send BT Meeting to activate Meeting Busy Tune for 1hr in English or BT Meeting T 3 to activate Meeting Busy Tune in Tamil for 3 hrs. Send BT to 369 for list of busy tunes.";

				$lang=$slang;
				$feature="BUSYTUNES";
				$MsgID="1047";
				&SendConfSMS;

				exit;
			}
		}
	}
	elsif($argcnt==2)
	{
		@langs=('s','e','t','sinhala','english','tamil');
		$match=0;
		foreach $lang (@langs)
		{
			if($array[1] eq $lang) { $match=1; last; }
		}

		if($match==1) 
		{
			$bttype=$array[0];
			$btlang=$array[1];
			$bttime="1";
		}
		elsif($array[1] =~ m/[0-9]/)
		{
			$bttype=$array[0];
			$bttime=$array[1];
			$btlang="e";
		}
		else
		{
			$bttype= $array[0].' '.$array[1];
			$btlang="e";
			$bttime="1";
		}
	}
	elsif($argcnt==1)
	{
		@langs=('s','e','t','sinhala','english','tamil');
		$match=0;
		foreach $lang (@langs)
		{
			if($array[0] eq $lang) { $match=1; last; }
		}

		if($match==1) 
		{
			#$message="Send HT<space>TuneId for activating Hello Tune or BT<space>name to 369 to activate a Busy Tune.";

			$lang=$slang;
			$feature="BUSYTUNES";
			$MsgID="1044";
			&SendConfSMS;

			exit;
		}
		elsif($array[0] =~ m/[0-9]/)
		{
			#$message="Send HT<space>TuneId for activating Hello Tune or BT<space>name to 369 to activate a Busy Tune.";

			$lang=$slang;
			$feature="BUSYTUNES";
			$MsgID="1044";
			&SendConfSMS;

			exit;
		}
		else
		{
			$bttype=$array[0];
			$btlang="e";
			$bttime="1";
		}
	}

	if($btlang eq "s" || $btlang eq "sinhala")
	{
		$btlang="S";
	}
	elsif($btlang eq "t" || $btlang eq "tamil")
	{
		$btlang="T";
	}
	elsif($btlang eq "e" || $btlang eq "english")
	{
		$btlang="E";
	}


	$bttime=int($bttime);

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select tunenumber,tunetype,btunetype,btlang,keyword,duration,contprov from smsbusytunes where keyword='$bttype' and substr(btlang,1,1)='$btlang' limit 1");
	$str->execute;
	$btcnt=$str->rows;
	@btsmstunes=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$tunenumber=$btsmstunes[0];
	$tunetype=$btsmstunes[1];
	$btunetype=$btsmstunes[2];
	$btlang=$btsmstunes[3];
	$keyword=$btsmstunes[4];
	$duration=$btsmstunes[5];
	$contprov=$btsmstunes[6];

	if($btcnt==1)
	{
		if($duration eq "DAY" && ($bttime<=0 || $bttime>10))
		{
			#$message="Busy Tunes can be activated for a maximum of 10 Days.";

			$lang=$slang;
			$feature="BUSYTUNES";
			$MsgID="1045";
			&SendConfSMS;

			exit;
		}
		elsif($duration eq "HOUR" && ($bttime<=0 || $bttime>23))
		{
			#$message="Busy Tunes can be activated for a maximum of 23 Hours.";

			$lang=$slang;
			$feature="BUSYTUNES";
			$MsgID="1046";
			&SendConfSMS;

			exit;
		}

		if($valid>0 && $btactivate==1)
		{
			$amount=0;
		}
		elsif($valid<=0 || $btactivate==2) 
		{
			if($prepos==0)
			{
				$amount="3.19";
			}
			elsif($prepos==1)
			{
				&BTsubscription;
			}
		}

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tuneid,substr(tunelang,1,1),substr(tunetype,1,1),contprov) as MTRcomment from contentprovider where tunenumber='$tunenumber' and tunetype='$tunetype'");
		$str->execute;
		$MTRcomment=$str->fetchrow();
		$str->finish();

		$str=$mysql->prepare("select now() + INTERVAL $bttime $duration");
		$str->execute;
		$expdate=$str->fetchrow();
		$str->finish();

		$mysql->disconnect();

		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',1,'$amount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$prepos')");
		$bsql->disconnect();

		$agent=LWP::UserAgent->new;
		$request=POST "http://192.168.100.28/inbilling/WebForm1.aspx?msisdn=$mobno&amount=$amount&tunetype=$tunetype&tunenumber=$tunenumber&billsrc=2&CP=$MTRcomment&subtype=$subcriptiontype&subtypename=$subtypename";
		$response=$agent->request($request);
		$rep=$response->as_string;
		@extract=split('\\n',$rep);
		$retval=$extract[$#extract];
		
		#$retval=4;	
	
		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("update billing set date=now(),status='$retval' where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and status=0 and date(date)=curdate() and amount='$amount' order by date desc limit 1");
		$bsql->disconnect();

		if($busysubcount==0)
		{
			$subscridate=`date "+%F %T"`;
			chomp($subscridate);
		}
		elsif($busysubcount==1)
		{
			if($userstatus eq "N")
			{
				$subscridate=`date "+%F %T"`;
				chomp($subscridate);
			}
		}

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$mysql->do("insert into existnewsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,amount,HTservice,MTRcomment,prepos) values ('$mobno','$slang','$tunenumber','$tunetype',now(),'$expdate',1,'$subscridate','$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$amount',1,'$MTRcomment','$prepos')");
		$mysql->disconnect();

		if($retval==1)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			$str=$mysql->prepare("select count(*) from busytunes where mobno='$mobno'");
			$str->execute;
			$busycnt=$str->fetchrow();
			$str->finish();

			if($busycnt==0)
			{
				$mysql->do("insert into busytunes(mobno,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',1,'$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$prepos')");
			}
			else
			{
				$mysql->do("update busytunes set tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',activate=1,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',billed='$retval',prepos='$prepos' where mobno='$mobno'"); 
			}

			$mysql->do("insert into busytunesmis(mobno,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,userstatus,billed,amount,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',1,'$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$amount','$prepos')");

			$mysql->disconnect();

			if($duration eq "HOUR")
			{
				if($bttime==1)
				{
					$period="$bttime"." Hr";
				}
				else
				{
					$period="$bttime"." Hrs";
				}
			}
			elsif($duration eq "DAY")
			{
				if($bttime==1)
				{
					$period="$bttime"." Day";
				}
				else
				{
					$period="$bttime"." Days";
				}
			}

			$hrday=substr($duration,0,1);

			if($valid>0 && $btactivate==1)
			{
				if($prepos==0 || $prepos==1)
				{
					$Response="$bttime"."$hrday"."1";
				}
			}
			elsif($valid<=0 || $btactivate==2)
			{
				if($prepos==0)
				{
					$Response="$bttime"."$hrday"."0";
				}
			}

			if($bttime==1)
			{
				if($Response eq "1H1")
				{
					#$message="Dear Customer your Busy Tune will be active for 1Hr. To deactivate send BT DA to 369. Thank You.";

					$MsgID="1055";
				}
				elsif($Response eq "1D1")
				{
					#$message="Dear Customer your Busy Tune will be active for 1 Day. To deactivate send BT DA to 369. Thank You.";

					$MsgID="1057";
				}
				elsif($Response eq "1H0")
				{
					#$message="Dear Customer your Busy Tune will be active for 1Hr and you will charged Two Rupees %26 Fifty cents plus Taxes. To deactivate send BT DA to 369. Thank You.";

					$MsgID="1059";
				}
				elsif($Response eq "1D0")
				{
					#$message="Dear Customer your Busy Tune will be active for 1 Day and you will charged Two Rupees %26 Fifty cents plus Taxes. To deactivate send BT DA to 369. Thank You.";
						  
					$MsgID="1061";
				}
			}
			elsif($bttime>1 && ($valid>0 && $btactivate==1))
			{
				if($hrday eq "H")
				{
					#$message="Dear Customer your Busy Tune will be active for $bttime Hrs. To deactivate send BT DA to 369. Thank You.";

					$MsgID="1056";
				}
				elsif($hrday eq "D")
				{
					#$message="Dear Customer your Busy Tune will be active for $bttime Days. To deactivate send BT DA to 369. Thank You.";

					$MsgID="1058";
				}
			}
			elsif($bttime>1 && ($valid<=0 || $btactivate==2))
			{
				if($hrday eq "H")
				{
					#$message="Dear Customer your Busy Tune will be active for $bttime Hrs and you will charged Two Rupees %26 Fifty cents plus Taxes. To deactivate send BT DA to 369. Thank You.";

					$MsgID="1060";
				}
				elsif($hrday eq "D")
				{
					#$message="Dear Customer your Busy Tune will be active for $bttime Days and you will charged Two Rupees %26 Fifty cents plus Taxes. To deactivate send BT DA to 369. Thank You.";

					$MsgID="1062";
				}
			}

			$lang=$slang;
			$feature="BUSYTUNES";
			&SendConfSMS;

			exit;
		}
		elsif($retval>1) 
		{
			#$message="Your tune request has failed due to low balance. Please recharge your account and try again. Thank you.";

			$lang=$slang;
			$feature="BUSYTUNES";
			$MsgID="1064";
			&SendConfSMS;

			exit;
		}
	}
	else
	{
		$btlanguages='';
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$stm=$mysql->prepare("select substr(btlang,1,1),btlang from smsbusytunes where keyword='$bttype'");
		$stm->execute;
		$btlangcnt=$stm->rows;
		while(@btlangs=$stm->fetchrow())
		{
			$btlanguages="$btlanguages"."$btlangs[0]";
			push(@busylangs,$btlangs[1]);
		}
		$stm->finish();
		$mysql->disconnect();

		if($btlangcnt>0)
		{
			foreach $tlang (@busylangs)
			{
				$langs=substr($tlang,0,1);
				$languages="$languages"."$langs";
			}

			if($languages eq "E")
			{
				$MsgID="1048";
			}
			elsif($languages eq "S")
			{
				$MsgID="1049";
			}
			elsif($languages eq "T")
			{
				$MsgID="1050";
			}
			elsif($languages eq "ES")
			{
				$MsgID="1051";
			}
			elsif($languages eq "ET")
			{
				$MsgID="1052";
			}
			elsif($languages eq "TS")
			{
				$MsgID="1053";
			}
			elsif($languages eq "STE")
			{
				$MsgID="1054";
			}

			$lang=$slang;
			$feature="BUSYTUNES";
			&SendConfSMS;

#			@busylangs=join(',',@busylangs);
#			$message="Requested Busy Tune is only available in @busylangs";

			exit;
		}
		else
		{
			#$message="Send BT Meeting to activate Meeting Busy Tune for 1hr in English or BT Meeting T 3 to activate Meeting Busy Tune in Tamil for 3 hrs. Send BT to 369 for list of busy tunes.";

			$lang=$slang;
			$feature="BUSYTUNES";
			$MsgID="1047";
			&SendConfSMS;

			exit;
		}
	}
}


sub BTsubscription
{
	$bamount="25.51";
	$btunenumber="100000";
	$btunetype="BUSY";
	$freetune="0";
	$promoid="0";
	$rcvmessage="BT SUB";

	$MTRcomment= "CRBT SN 100000 S B HUTCH";

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select curdate() + INTERVAL 30 DAY ");
	$str->execute;
	$btsexpdate=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
	$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,freetune,promoid,prepos) values ('$mobno','$btunenumber','$btunetype',now(),'$btsexpdate',1,'$bamount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$freetune','$promoid','$prepos')");
	$bsql->disconnect();

	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/inbilling/WebForm1.aspx?msisdn=$mobno&amount=$bamount&tunetype=$btunetype&tunenumber=$btunenumber&billsrc=2&CP=$MTRcomment&subtype=$subcriptiontype&subtypename=$subtypename";
	$response=$agent->request($request);
	$rep=$response->as_string;
	@extract=split('\\n',$rep);
	$retval=$extract[$#extract];

	$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
	$bsql->do("update billing set date=now(),status='$retval' where mobno='$mobno' and tunenumber='$btunenumber' and tunetype='$btunetype' and status=0 and date(date)=curdate() and amount='$bamount' order by date desc limit 1");
	$bsql->disconnect();

	if($busysubcount==0)
	{
		$subscridate=`date "+%F %T"`;
		chomp($subscridate);
	}
	elsif($busysubcount==1)
	{
		if($userstatus eq "N")
		{
			$subscridate=`date "+%F %T"`;
			chomp($subscridate);
		}
	}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$mysql->do("insert into existnewsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,amount,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','$slang','$btunenumber','$btunetype',now(),'$btsexpdate',1,'$subscridate','$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$bamount',1,'$MTRcomment','$freetune','$promoid','$prepos')");
	$mysql->disconnect();

	if($retval==1)
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		if($busysubcount==0)
		{
			 $mysql->do("insert into BTsubscriber (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,freetune,promoid,prepos) values ('$mobno','$slang','$btunenumber','$btunetype',now(),'$btsexpdate',1,now(),'$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$freetune','$promoid','$prepos')");
		}
		elsif($busysubcount==1)
		{
			$mysql->do("update BTsubscriber set lang='$slang',tunenumber='$btunenumber',tunetype='$btunetype',date=now(),expdate='$btsexpdate',activate=1,subscridate=now(),subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',userstatus='$userstatus',billed='$retval',freetune='$freetune',promoid='$promoid',prepos='$prepos' where mobno='$mobno'");
		}

		$mysql->do("insert into BTsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,amount,freetune,promoid,prepos) values ('$mobno','$slang','$btunenumber','$btunetype',now(),'$btsexpdate',1,now(),'$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$bamount','$freetune','$promoid','$prepos')");

		$mysql->disconnect();

		#$message="Dear Customer, U have successfully subscribed for Busy tunes. You will be charged with a subscription of Rs. 20 %2B taxes valid for 30 days.";

		$lang=$slang;
		$feature="BUSYTUNES";
		$MsgID="1068";
		&SendConfSMS;

		$amount=0;
	}
	elsif($retval>1)
	{
		#$message="Your subscription request has failed due to low balance. Please recharge your account and try again. Thank you.";

		$lang=$slang;
		$feature="BUSYTUNES";
		$MsgID="1069";
		&SendConfSMS;

		exit;
	}

	$str=$mysql->prepare("select count(*),(CASE 1 WHEN DATEDIFF(expdate,curdate()) is NULL THEN 0 ELSE DATEDIFF(expdate,curdate()) END) from BTsubscriber where mobno='$mobno'");
	$str->execute;
	@busyvalid=$str->fetchrow();
	$str->finish();

	$busysubcount=$busyvalid[0];
	$valid=$busyvalid[1];

	if($valid>0 && $btactivate==1)
	{
		$amount=0;
	}
}



sub CTDA
{
	$mobno=substr($mobno,-9,9);

	$sid=1;
	$subcriptiontype="8";
	$subtypename="SMS";

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1041";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to deactivate your CopyTune service, since you are Pre activated with Corporate tune.Thank you. Hutch";

		$MsgID="1040";
		&SendConfSMS;

		exit;
	}

	################################################# CHECK CORPORATE TUNE #################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select sno,tunenumber,tunetype from copytune where callerid='$mobno' and activate=1 and timediff(now(),insdate)<'00:15:00' and topick=0 order by date limit 1 ");
	$str->execute;
	$copycnt=$str->rows;
	@copytune=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$sno=$copytune[0];
	$tunenumber=$copytune[1];
	$tunetype=$copytune[2];

	if($copycnt==1)
	{
		$userstatus='E';

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$mysql->do("insert into deactivated (mobno,lang,tunenumber,tunetype,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),2,'$subcriptiontype','CT','$sid','$prepos')");
		$mysql->do("update copytune set date=now(),activate=2 where sno='$sno'");
		$mysql->disconnect();

		#$message="You have successfully Deactivated your Copy tune. Thank you for using Hello Tunes. Good bye !";

		$MsgID="1038";
		&SendConfSMS;

		exit;
	}
	elsif($copycnt==0)
	{
		#$message="Sorry. You do not copied any tune for this Number within past 15 mins. Thank you. Hutch";
		$userstatus='E';

		$MsgID="1039";
		&SendConfSMS;

		exit;
	}
	else 
	{
		#$message="Server Busy, please try later.";
		$userstatus='E';

		$MsgID="1041";
		&SendConfSMS;

		exit;
	}
}


sub NTNAME
{
	$mobno=substr($mobno,-9,9);
	$name =~ tr/\$#@~!&*"'%\-_=+()[]{}<>;.,:?^ `\|\\\///d;

	$style="1";
	$sid="1";
	$subcriptiontype="8";
	$subtypename="NAME";

	$lang="3";
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select lang from existnewsubscriber where mobno='$mobno'");
	$str->execute;
	$lang=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($lang eq '' || $lang==0) {$lang="3";}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from NameCRBTTestDNs where mobno='$mobno' and enable=1");
	$str->execute;
	$enablecnt=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($enablecnt==1)
	{}
	elsif($enablecnt==0)
	{
		exit;
	}

	if($name eq '')
	{
		#$message="Server Busy, please try again later.";

		$topick="0";
		$style="0";

		$feature="NAMETUNES";
		$MsgID="1088";
		&SendConfSMS;

		exit;
	}

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$topick="0";
		$style="0";

		$feature="NAMETUNES";
		$MsgID="1088";
		&SendConfSMS;

		exit;
	}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from NameCRBT where mobno='$mobno' and activate=1");
	$str->execute;
	$subscnt=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($subscnt==0)
	{
		$userstatus='N';
	}
	elsif($subscnt==1)
	{
		$userstatus='E';
	}

	############################################## CHECK DUPLICATE NAME REQUEST ##############################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from NameCRBTSMS where mobno='$mobno' and insdate between now() - INTERVAL 24 HOUR and now() and name='$name' and topick=2");
	$str->execute;
	$dupcnt=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($dupcnt==1)
	{
		#$message="Dear Customer, the Name Tune you requested is under processing. Thank you. Hutch";

		$topick="9";
		$style="0";

		$feature="NAMETUNES";
		$MsgID="1087";
		&SendConfSMS;

		exit;
	}

	############################################## CHECK DUPLICATE NAME REQUEST ##############################################


	################################################## CHECK CORPORATE TUNE ##################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to activate the requested Name Tune since u r Pre activated with Corporate tune. When this expires U will be enabled for normal activation.";

		$topick="6";
		$style="0";
		$name='';

		$feature="NAMETUNES";
		$MsgID="1086";
		&SendConfSMS;

		exit;
	}

	################################################## CHECK CORPORATE TUNE ##################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from NameCRBTtunes where nametune like '$name%'");
	$str->execute;
	$cnt=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($cnt>0)
	{
		#$message="Dear customer, we have got your Name Tune request you will receive matching available names shortly. Thank you.";

		$topick="1";
		$style="1";

		$feature="NAMETUNES";
		$MsgID="1084";
		&SendConfSMS;

		$str=$mysql->prepare("select nametune from NameCRBTmis where mobno='$mobno' and activate=1 and nametune='$name' order by date desc limit 1");
		$str->execute;
		$prnametune=$str->fetchrow();
		$actcnt=$str->rows;
		$str->finish();
		$mysql->disconnect();

		if($actcnt==1)
		{
			push(@namelist,$prnametune);

			$message="Dear customer, to re-activates your existing Name Tune 1.$prnametune sms NTOPT<space><1> to 369. For new Name Tune sms NT <name> to 369 Thank you.";
		}
		else
		{
			$i="1";
			$message='';
			$seperator="/";
			$option="1";

			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			$str=$mysql->prepare("select nametune from NameCRBTtunes where nametune like '$name%'");
			$str->execute;
			while(@names=$str->fetchrow())
			{
				push(@namelist,$names[0]);

				if($i>1)
				{
					$option="$option"."$seperator"."$i";
				}

				$message="$message"."$i"."."."$names[0] ";

				$i++;
			}
			$str->finish();

			$mysql->disconnect();

			chop($message);

			$message="$message".". Please send NTOPT<space><$option> to 369. Thank you.";
		}

		$topick="1";
		$style="1";

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$mysql->do("insert into NameCRBTresplogs(mobno,date,name1,name2,name3,name4,name5,name6,name7,name8,name9,name10,userstatus,prepos) values ('$mobno',now(),'$namelist[0]','$namelist[1]','$namelist[2]','$namelist[3]','$namelist[4]','$namelist[5]','$namelist[6]','$namelist[7]','$namelist[8]','$namelist[9]','$userstatus','$prepos')");
		$mysql->do("insert into NameCRBTSMS (mobno,lang,name,date,response,subcriptiontype,subtypename,serverid,topick,style,userstatus,prepos) values ('$mobno','$lang','$name',now(),'$message','$subcriptiontype','$subtypename','$sid','$topick','$style','$userstatus','$prepos')");

		$mysql->disconnect();

		$agent=LWP::UserAgent->new;        
		$send=POST "http://192.168.100.105:80/SENDSMS/sendsms.jsp?mobno=$mobno&Message=$message&ShortCode=$shortcode&Priority=1";
		$agent->request($send);
        
		exit;
	}
	else
	{
		$message="Name Tune you have requested is not available presently. You will be intimated once the requested Name Tune is available within 24 hours. Thank you.";

		$topick="2";
		$style="1";

		$feature="NAMETUNES";
		$MsgID="1085";
		&SendConfSMS;

		exit;
	}
}



sub NTOPT
{
	$mobno=substr($mobno,-9,9);

	$style="1";
	$expdays="30";
	$sid="1";
	$freetune="0";
	$promoid="0";
	$amount="0";
	$subcriptiontype="8";
	$subtypename="NAME";

	$lang="3";
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select lang from existnewsubscriber where mobno='$mobno'");
	$str->execute;
	$lang=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($lang eq '' || $lang==0) {$lang="3";}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from NameCRBTTestDNs where mobno='$mobno' and enable=1");
	$str->execute;
	$enablecnt=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($enablecnt==1)
	{}
	elsif($enablecnt==0)
	{
		exit;
	}

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$topick="0";
		$style="0";

		$feature="NAMETUNES";
		$MsgID="1091";
		&SendConfSMS;

		exit;
	}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from NameCRBT where mobno='$mobno' and activate=1");
	$str->execute;
	$subscnt=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($subscnt==0)
	{
		$userstatus='N';
	}
	elsif($subscnt==1)
	{
		$userstatus='E';
	}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select name$reply from NameCRBTresplogs where mobno='$mobno' and topick=0 order by sno desc limit 1");
	$str->execute;
	$snametune=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($snametune eq "NULL" || $snametune eq '')
	{
		#$message="Dear customer, invalid request, please send correct keyword for getting Name Tunes sms NT <name> to 369.";

		$topick="4";
		$style="1";
		$name=$snametune;

		$feature="NAMETUNES";
		$MsgID="1090";
		&SendConfSMS;

		exit;
	}
	else
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$str=$mysql->prepare("select count(*) from NameCRBT where mobno='$mobno' and activate=1");
		$str->execute;
		$namecnt=$str->fetchrow();
		$str->finish();

		$str=$mysql->prepare("select tunenumber,tunetype from NameCRBTtunes where nametune='$snametune'");
		$str->execute;
		@nametune=$str->fetchrow();
		$str->finish();

		$tunenumber=$nametune[0];
		$tunetype=$nametune[1];

		$str=$mysql->prepare("select concat_ws(' ','CRBT SN',tunenumber,'S','M',contprov) as MTRcomment from NameCRBTtunes where tunenumber='$tunenumber' and tunetype='$tunetype'");
		$str->execute;
		$MTRcomment=$str->fetchrow();
		$str->finish();

		$mysql->disconnect();

		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,freetune,promoid,prepos) values ('$mobno','$tunenumber','$tunetype',now(),curdate() + INTERVAL '$expdays' DAY,1,'$amount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$freetune','$promoid','$prepos')");
		$bsql->disconnect();

		$agent=LWP::UserAgent->new;
		$request=POST "http://192.168.100.28/inbilling/WebForm1.aspx?msisdn=$mobno&amount=$amount&tunetype=$tunetype&tunenumber=$tunenumber&billsrc=2&CP=$MTRcomment&subtype=$subcriptiontype&subtypename=$subtypename";
		$response=$agent->request($request);
		$rep=$response->as_string;
		@extract=split('\\n',$rep);
		$retval=$extract[$#extract];

		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("update billing set date=now(),status='$retval' where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and status=0 and date(date)=curdate() and amount='$amount' order by date desc limit 1");
		$bsql->disconnect();

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$mysql->do("insert into existnewsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,amount,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','3','$tunenumber','$tunetype',now(),curdate() + INTERVAL '$expdays' DAY,1,now(),'$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$amount',1,'$MTRcomment','$freetune','$promoid','$prepos')");

		if($namecnt)         
		{
			$mysql->do("update NameCRBT set nametune='$snametune',tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate=curdate() + INTERVAL '$expdays' DAY,activate=1,subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',style='$style',userstatus='$userstatus',prepos='$prepos' where mobno='$mobno'");
		}
		else
		{
			$mysql->do("insert into NameCRBT (mobno,nametune,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,style,userstatus,prepos) values ('$mobno','$snametune','$tunenumber','$tunetype',now(),curdate() + INTERVAL '$expdays' DAY,1,'$subcriptiontype','$subtypename','$sid','$style','$userstatus','$prepos')");
		}

		$mysql->do("insert into NameCRBTmis (mobno,nametune,tunenumber,tunetype,date,expdate,activate,subcriptiontype,subtypename,serverid,style,userstatus,prepos) values ('$mobno','$snametune','$tunenumber','$tunetype',now(),curdate() + INTERVAL '$expdays' DAY,1,'$subcriptiontype','$subtypename','$sid','$style','$userstatus','$prepos')");

		$mysql->do("update NameCRBTresplogs set date=now(),reply='$reply',topick=1 where mobno='$mobno' order by sno desc limit 1");

		$message="Dear customer, the Name Tune requested has been activated successfully. Thank you.";

		$topick="5";
		$style="1";
		$mysql->do("insert into NameCRBTSMS (mobno,lang,name,tunenumber,tunetype,date,response,subcriptiontype,subtypename,serverid,topick,style,userstatus,prepos) values ('$mobno','$lang','$snametune','$tunenumber','$tunetype',now(),'$message','$subcriptiontype','$subtypename','$sid','$topick','$style','$userstatus','$prepos')");

		$mysql->disconnect();

		$agent=LWP::UserAgent->new;
		$send=POST "http://192.168.100.105:80/SENDSMS/sendsms.jsp?mobno=$mobno&Message=$message&ShortCode=$shortcode&Priority=1";
		$agent->request($send);

		exit;
	}
}



sub NTDA
{
	$mobno=substr($mobno,-9,9);

	$sid="1";
	$subcriptiontype="8";
	$subtypename="NAME";

	$lang="3";
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select lang from existnewsubscriber where mobno='$mobno'");
	$str->execute;
	$lang=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($lang eq '' || $lang==0) {$lang="3";}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from NameCRBTTestDNs where mobno='$mobno' and enable=1");
	$str->execute;
	$enablecnt=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($enablecnt==1)
	{}
	elsif($enablecnt==0)
	{
		exit;
	}

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$topick="0";
		$style="0";

		$feature="NAMETUNES";
		$MsgID="1095";
		&SendConfSMS;

		exit;
	}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from NameCRBT where mobno='$mobno' and activate=1");
	$str->execute;
	$subscnt=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($subscnt==0)
	{
		$userstatus='N';
	}
	elsif($subscnt==1)
	{
		$userstatus='E';
	}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),nametune,tunenumber,tunetype from NameCRBT where mobno='$mobno' group by mobno");
	$str->execute;
	@NameCRBT=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	$namecnt=$NameCRBT[0];
	$nametune=$NameCRBT[1];
	$tunenumber=$NameCRBT[2];
	$tunetype=$NameCRBT[3];

	################################################## CHECK CORPORATE TUNE ##################################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to deactivate your Name Tune, since you are Pre activated with Corporate tune. Thank you. Hutch";

		$topick="6";
		$style="0";
		$name='';

		$feature="NAMETUNES";
		$MsgID="1094";
		&SendConfSMS;

		exit;
	}

	################################################## CHECK CORPORATE TUNE ##################################################

	if($namecnt==0)
	{
		#$message="You are Already Deactivated, To Activate the Name Tunes sms NT <name> to 369.";

		$topick="7";
		$style="0";
		$name='';

		$feature="NAMETUNES";
		$MsgID="1093";
		&SendConfSMS;

		exit;
	}
	else
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

		$mysql->do("delete from NameCRBT where mobno='$mobno'");

		$mysql->do("insert into NameCRBTmis(mobno,nametune,tunenumber,tunetype,date,activate,subcriptiontype,subtypename,serverid,userstatus,prepos) values ('$mobno','$nametune','$tunenumber','$tunetype',now(),2,'$subcriptiontype','$subtypename','$sid','$userstatus','$prepos')");

		$mysql->do("insert into deactivated (mobno,lang,tunenumber,tunetype,date,activate,subcriptiontype,subtypename,serverid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),2,'$subcriptiontype','$subtypename','$sid','$prepos')");

		$message="You have successfully deactivated Name Tune. Thank you for using Name Tunes.";

		$topick="8";
		$style="0";
		$mysql->do("insert into NameCRBTSMS (mobno,lang,name,tunenumber,tunetype,date,response,subcriptiontype,subtypename,serverid,topick,style,userstatus,prepos) values ('$mobno','$lang','$nametune','$tunenumber','$tunetype',now(),'$message','$subcriptiontype','$subtypename','$sid','$topick','$style','$userstatus','$prepos')");

		$mysql->disconnect();

		$agent=LWP::UserAgent->new;
		$send=POST "http://192.168.100.105:80/SENDSMS/sendsms.jsp?mobno=$mobno&Message=$message&ShortCode=$shortcode&Priority=1";
		$agent->request($send);

		exit;
	}
}



sub SUBUT
{
	$mobno=substr($mobno,-9,9);

	$sid="1";
	$subcriptiontype="8";
	$subtypename="UTUNES";
	$freetune="0";
	$promoid="0";
	$RenewalFlag="0";

	$lang="3";
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select lang from existnewsubscriber where mobno='$mobno'");
	$str->execute;
	$lang=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($lang eq '' || $lang==0) {$lang="3";}

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1101";
		&SendConfSMS;

		exit;
	}

	################################# Check Customer is Active with Corportae Tune ################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to subscribe for Unlimited Tunes since U are Pre activated with corporate tune. When this expires U will be enabled for normal activation.";

		$MsgID="1100";
		&SendConfSMS;

		exit;
	}

	################################# Check Customer is Active with Corportae Tune ################################        
	
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*),(CASE 1 WHEN DATEDIFF(expdate,curdate()) is NULL THEN '0' ELSE DATEDIFF(expdate,curdate()) END) from ANYTunes where mobno='$mobno'");
	$str->execute;
	@ANYTunes=$str->fetchrow();
	$acount=$str->rows;
	$str->finish();
	$mysql->disconnect();

	$acount=$ANYTunes[0];
	$differ=$ANYTunes[1];

	if($acount==0)
	{
		$lang=3;
		$userstatus='N';
	}
	elsif($acount==1)
	{
		$userstatus='E';

		if($differ<=0)
		{
			$lang=3;
			$userstatus='N';
		}
		elsif($differ>0)
		{
			$userstatus='E';
		}
	}

	if($acount==1)
	{
		if($differ>0)
		{
			#$message="Dear customer u r already subscribed with Unlimited Tunes. Thank you. Hutch";

			$MsgID="1099";
			&SendConfSMS;

			exit;
		}
	}
	elsif($acount==0 || $differ<=0) 
	{
		$tunenumber="100001";
		$tunetype="UTUNES";

		$MTRcomment= "CRBT SN 100001 S U HUTCH";

		if($prepos==1)
		{
			$amount="191.33";

			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);               
			$str=$mysql->prepare("select curdate() + INTERVAL 30 DAY");
			$str->execute;
			$expdate=$str->fetchrow();
			$str->finish();
			$mysql->disconnect();
		}

		if($prepos==0) 
		{
			$amount="6.38";

			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
			$str=$mysql->prepare("select curdate() + INTERVAL 1 DAY");
			$str->execute;
			$expdate=$str->fetchrow();
			$str->finish();
			$mysql->disconnect();
		}

		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("insert into billing (mobno,tunenumber,tunetype,date,expdate,activate,amount,subcriptiontype,subtypename,userstatus,serverid,MTRcomment,freetune,promoid,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',1,'$amount','$subcriptiontype','$subtypename','$userstatus','$sid','$MTRcomment','$freetune','$promoid','$prepos')");
		$bsql->disconnect();

		$agent=LWP::UserAgent->new;
		$request=POST "http://192.168.100.28/inbilling/WebForm1.aspx?msisdn=$mobno&amount=$amount&tunetype=$tunetype&tunenumber=$tunenumber&billsrc=2&CP=$MTRcomment&subtype=$subcriptiontype&subtypename=$subtypename";
		$response=$agent->request($request);
		$rep=$response->as_string;
		@extract=split('\\n',$rep);
		$retval=$extract[$#extract];

		##$retval=4;$lang=2;

		$bsql=DBI->connect($dsnb,$dbuser,$dbpasswd);
		$bsql->do("update billing set date=now(),status='$retval' where mobno='$mobno' and tunenumber='$tunenumber' and tunetype='$tunetype' and status=0 and date(date)=curdate() and amount='$amount' order by date desc limit 1");
		$bsql->disconnect();

		if($acount==0)
		{
			$subscridate=`date "+%F %T"`;
			chomp($subscridate);
		}
		elsif($acount==1)
		{
			if($userstatus eq "N")
			{
				$subscridate=`date "+%F %T"`;
				chomp($subscridate);
			}
		}

		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$mysql->do("insert into existnewsubscribermis (mobno,lang,tunenumber,tunetype,date,expdate,activate,subscridate,subcriptiontype,subtypename,serverid,userstatus,billed,amount,HTservice,MTRcomment,freetune,promoid,prepos) values ('$mobno','$lang','$tunenumber','$tunetype',now(),'$expdate',1,'$subscridate','$subcriptiontype','$subtypename','$sid','$userstatus','$retval','$amount',1,'$MTRcomment','$freetune','$promoid','$prepos')");
		$mysql->disconnect();

		if($retval==1)
		{
			$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

			if($acount==0)
			{
				$mysql->do("insert into ANYTunes (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,category,userstatus,subcriptiontype,subtypename,serverid,billed,RenewalFlag,freetune,promoid,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,1,'$userstatus','$subcriptiontype','$subtypename','$sid','$retval','$RenewalFlag','$freetune','$promoid','$prepos')");
			}
			elsif($acount==1)
			{
				$mysql->do("update ANYTunes set tunenumber='$tunenumber',tunetype='$tunetype',date=now(),expdate='$expdate',sdate=now(),playdate='$expdate',activate=1,category=1,userstatus='$userstatus',subcriptiontype='$subcriptiontype',subtypename='$subtypename',serverid='$sid',billed='$retval',RenewalFlag='$RenewalFlag',freetune='$freetune',promoid='$promoid',prepos='$prepos' where mobno='$mobno'");
			}

			$mysql->do("insert into ANYTunesmis (mobno,tunenumber,tunetype,date,expdate,sdate,playdate,activate,category,userstatus,subcriptiontype,subtypename,serverid,billed,amount,RenewalFlag,freetune,promoid,prepos) values ('$mobno','$tunenumber','$tunetype',now(),'$expdate',now(),'$expdate',1,1,'$userstatus','$subcriptiontype','$subtypename','$sid','$retval','$amount','$RenewalFlag','$freetune','$promoid','$prepos')");

			$mysql->disconnect();

			if($prepos==1)
			{
				#$message="Dear Customer, U have successfully subscribed for Unlimited Tunes %26 have been charged Rs 150 %2B taxes valid for 30 days. Call 369 for Unlimited Tunes.";

				$MsgID="1096";
				&SendConfSMS;

				exit;
			}
			elsif($prepos==0)
			{
				#$message="You have been charged with 5 Rupees plus taxes valid till end of day and tune will auto renew from tomorrow on a daily basis. Thank you for using Hutch.";

				$MsgID="1097";
				&SendConfSMS;

				exit;
			}
		}
		elsif($retval>1)
		{
			#$message="Your subscription request has failed due to low balance. Please recharge your account and try again. Thank you.";

			$MsgID="1098";
			&SendConfSMS;

			exit;
		}
	}
}



sub UNSUBUT
{
	$mobno=substr($mobno,-9,9);

	$sid="1";
	$subcriptiontype="8";
	$subtypename="UTUNES";
	$freetune="0";
	$promoid="0";

	$lang="3";
	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select lang from existnewsubscriber where mobno='$mobno'");
	$str->execute;
	$lang=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($lang eq '' || $lang==0) {$lang="3";}

	$prepos="3";
	$agent=LWP::UserAgent->new;
	$request=POST "http://192.168.100.28/GetDNStatus/WebForm1.aspx?msisdn=$mobno";
	$response=$agent->request($request);
	$prepos=$response->content;

	if($prepos==0 || $prepos==1)
	{}
	else
	{
		#$message="Server Busy, please try again later.";

		$MsgID="1105";
		&SendConfSMS;

		exit;
	}

	################################# Check Customer is Active with Corportae Tune ################################

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from CORPTUNEpromo where mobno='$mobno' and activate=1 and billed=1 and subcriptiontype=10 and subtypename='CORP'");
	$str->execute;
	$Corpcount=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($Corpcount==1)
	{
		#$message="We are unable to unsubscribe UR Unlimited Tunes service since u r Pre activated with corporate tune. When this expires U will be enabled for normal activation.";

		$MsgID="1104";
		&SendConfSMS;

		exit;
	}

	################################# Check Customer is Active with Corportae Tune ################################        

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
	$str=$mysql->prepare("select count(*) from ANYTunes where mobno='$mobno'");
	$str->execute;
	$count=$str->fetchrow();
	$str->finish();
	$mysql->disconnect();

	if($count==0)
	{
		#$message="You are not a subscriber of Unlimited Tunes. To Activate the service please send SUB UT to 369. Charges Apply.";

		$MsgID="1103";
		&SendConfSMS;

		exit;
	}
	elsif($count==1)
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$mysql->do("delete from ANYTunes where mobno='$mobno'");
		$mysql->do("insert into ANYTunesmis (mobno,date,activate,category,userstatus,subcriptiontype,subtypename,serverid,prepos) values ('$mobno',now(),2,1,'E','$subcriptiontype','$subtypename','$sid','$prepos')");
		$mysql->do("insert into deactivated (mobno,lang,date,activate,subcriptiontype,subtypename,serverid) values ('$mobno','$lang',now(),2,'$subcriptiontype','$subtypename','$sid')");
		$mysql->disconnect();

		#$message="Your Unlimited Tunes service has been deactivated successfully. Thank you.";

		$MsgID="1102";
		&SendConfSMS;

		exit;

	}
}


sub GTSONGNAME
{
	$promoid="0";
	$strlen=length($songname);
	$rcvsongname=$songname;

	if($strlen<3)
	{
		#$message="Please send the proper keyword.";

		$MsgID="1037";
		&SendConfSMS;

		exit;
	}
	elsif($strlen>=3)
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$str=$mysql->prepare("select trim(songname),tuneid from contentprovider where ivrno<>0 and IsValid=1 and songname like '\%$songname\%' and (tunetype like 'PR%' OR tunetype like 'NPR%') order by ivrno limit 1");
		$str->execute;
		$count=$str->rows;
		@tunes=$str->fetchrow();
		$str->finish();
		$mysql->disconnect();

		$songname=$tunes[0];
		$tuneid=$tunes[1];

		if($count>0)
		{
			#$message="To activate <SONGNAME> as your Hello Tune, dial 369<TUNEID>.";

			$MsgID="1268";
			&SendConfSMS;

			exit;
		}
		elsif($count==0)
		{
			$songname=$rcvsongname;
			#$message="Sorry! Song name <SONGNAME> not found. Please check the spelling or try a different song.";

			$MsgID="1269";
			&SendConfSMS;

			exit;
		}
	}
}



sub SendConfSMS
{
	if($lang==1 || $lang==2 || $lang==3)
	{}
	else
	{
		$lang=3;
	}

	if($mobno==789688118 || $mobno==782737445 || $mobno==788323803)
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$str=$mysql->prepare("select message from ConfirmationSMS where MsgID='$MsgID' and lang='$lang'");
		$str->execute;
		$message=$str->fetchrow();
		$str->finish();
		$mysql->disconnect();
	}
	else
	{
		$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);
		$str=$mysql->prepare("select message from ConfirmationSMS where MsgID='$MsgID' and lang='$lang'");
		$str->execute;
		$message=$str->fetchrow();
		$str->finish();
		$mysql->disconnect();
	}

	if($HELP==1)
	{
		$HELP="0";
	}
	else
	{
		$message=~s/\%/%25/g;
		$message=~s/\&/%26/g;
		$message=~s/\+/%2B/g;

		$message=~s/\<BILLEDAMOUNT\>/$billeddays/g;
		$message=~s/\<EXPIRYDAYS\>/$nobdays/g;
		$message=~s/\<PERIOD\>/$period/g;
		$message=~s/\<GIFTMOBNO\>/$assignto/g;
		$message=~s/\<MOBNO\>/$assignto/g;
		$message=~s/\<GROUPNUMBER\>/$grpnumber/g;
		$message=~s/\<NUMBER\>/$bttime/g;
		$message=~s/\<SONGNAME\>/\"$songname\"/g;
		$message=~s/\<TUNEID\>/$tuneid/g;
	}

	$mysql=DBI->connect($dsn,$dbuser,$dbpasswd);

	if($feature eq "BUSYTUNES")
	{
		$mysql->do("insert into BUSYSMSresplogs (mobno,MsgID,lang,message,date,response,status,subcriptiontype,subtypename,userstatus,serverid,prepos) values ('$mobno','$MsgID','$lang','$rcvmessage',now(),'$message',1,'$subcriptiontype','$subtypename','$userstatus','$sid','$prepos')");
	}
	elsif($feature eq "NAMETUNES")
	{
		$mysql->do("insert into NameCRBTSMS (mobno,MsgID,lang,name,date,response,subcriptiontype,subtypename,serverid,topick,style,userstatus,prepos) values ('$mobno','$MsgID','$lang','$name',now(),'$message','$subcriptiontype','$subtypename','$sid','$topick','$style','$userstatus','$prepos')");
	}
	else
	{
		$mysql->do("insert into SMSresplogs (mobno,MsgID,lang,date,response,status,subcriptiontype,subtypename,userstatus,serverid,prepos) values ('$mobno','$MsgID','$lang',now(),'$message',1,'$subcriptiontype','$subtypename','$userstatus','$sid','$prepos')");
	}

	$mysql->do("insert into SendConfSMS (mobno,MsgID,lang,date,message,subcriptiontype,subtypename,userstatus,serverid,promoid,prepos) values ('$mobno','$MsgID','$lang',now(),'$message','$subcriptiontype','$subtypename','$userstatus','$sid','$promoid','$prepos')");

	$mysql->disconnect();

	$agent=LWP::UserAgent->new;
	$send=POST "http://192.168.100.105:80/SENDSMS/sendsms.jsp?mobno=$mobno&Message=$message&ShortCode=$shortcode&Priority=1";
	$agent->request($send);
}

