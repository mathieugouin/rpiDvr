#!/usr/bin/perl -w

use List::Util 'any';

#
# The categories recognized by tvheadend (see epg.c)
#

my $MOVIE             =    "Movie / Drama";
my $THRILLER          =    "Detective / Thriller";
my $ADVENTURE         =    "Adventure / Western / War";
my $SF                =    "Science fiction / Fantasy / Horror";
my $COMEDY            =    "Comedy";
my $SOAP              =    "Soap / Melodrama / Folkloric";
my $ROMANCE           =    "Romance";
my $HISTORICAL        =    "Serious / Classical / Religious / Historical movie / Drama";
my $XXX               =    "Adult movie / Drama";

my $NEWS              =    "News / Current affairs";
my $WEATHER           =    "News / Weather report";
my $NEWS_MAGAZINE     =    "News magazine";
my $DOCUMENTARY       =    "Documentary";
my $DEBATE            =    "Discussion / Interview / Debate";
my $INTERVIEW         =    $DEBATE ;

my $SHOW              =    "Show / Game show";
my $GAME              =    "Game show / Quiz / Contest";
my $VARIETY           =    "Variety show";
my $TALKSHOW          =    "Talk show";

my $SPORT             =    "Sports";
my $SPORT_SPECIAL     =    "Special events (Olympic Games; World Cup; etc.)";
my $SPORT_MAGAZINE    =    "Sports magazines";
my $FOOTBALL          =    "Football / Soccer";
my $TENNIS            =    "Tennis / Squash";
my $SPORT_TEAM        =    "Team sports (excluding football)";
my $ATHLETICS         =    "Athletics";
my $SPORT_MOTOR       =    "Motor sport";
my $SPORT_WATER       =    "Water sport";

my $KIDS              =    "Children's / Youth programmes";
my $KIDS_0_5          =    "Pre-school children's programmes";
my $KIDS_6_14         =    "Entertainment programmes for 6 to 14";
my $KIDS_10_16        =    "Entertainment programmes for 10 to 16";
my $EDUCATIONAL       =    "Informational / Educational / School programmes";
my $CARTOON           =    "Cartoons / Puppets";

my $MUSIC             =    "Music / Ballet / Dance";
my $ROCK_POP          =    "Rock / Pop";
my $CLASSICAL         =    "Serious music / Classical music";
my $FOLK              =    "Folk / Traditional music";
my $JAZZ              =    "Jazz";
my $OPERA             =    "Musical / Opera";

my $CULTURE           =    "Arts / Culture (without music)";
my $PERFORMING        =    "Performing arts";
my $FINE_ARTS         =    "Fine arts";
my $RELIGION          =    "Religion";
my $POPULAR_ART       =    "Popular culture / Traditional arts";
my $LITERATURE        =    "Literature";
my $FILM              =    "Film / Cinema";
my $EXPERIMENTAL_FILM =    "Experimental film / Video";
my $BROADCASTING      =    "Broadcasting / Press";

my $SOCIAL            =    "Social / Political issues / Economics";
my $MAGAZINE          =    "Magazines / Reports / Documentary";
my $ECONOMIC          =    "Economics / Social advisory";
my $VIP               =    "Remarkable people";

my $SCIENCE           =    "Education / Science / Factual topics";
my $NATURE            =    "Nature / Animals / Environment";
my $TECHNOLOGY        =    "Technology / Natural sciences";
my $MEDECINE          =    "Medicine / Physiology / Psychology";
my $FOREIGN           =    "Foreign countries / Expeditions";
my $SPIRITUAL         =    "Social / Spiritual sciences";
my $FURTHER_EDUCATION =    "Further education";
my $LANGUAGES         =    "Languages";

my $HOBBIES           =    "Leisure hobbies";
my $TRAVEL            =    "Tourism / Travel";
my $HANDICRAF         =    "Handicraft";
my $MOTORING          =    "Motoring";
my $FITNESS           =    "Fitness and health";
my $COOKING           =    "Cooking";
my $SHOPPING          =    "Advertisement / Shopping";
my $GARDENING         =    "Gardening";


#
# Array containing all default tvheadend category supported
#
my @TVH_CATEGORY = (
  $MOVIE             ,
  $THRILLER          ,
  $ADVENTURE         ,
  $SF                ,
  $COMEDY            ,
  $SOAP              ,
  $ROMANCE           ,
  $HISTORICAL        ,
  $XXX               ,

  $NEWS              ,
  $WEATHER           ,
  $NEWS_MAGAZINE     ,
  $DOCUMENTARY       ,
  $DEBATE            ,
  $INTERVIEW         ,

  $SHOW              ,
  $GAME              ,
  $VARIETY           ,
  $TALKSHOW          ,

  $SPORT             ,
  $SPORT_SPECIAL     ,
  $SPORT_MAGAZINE    ,
  $FOOTBALL          ,
  $TENNIS            ,
  $SPORT_TEAM        ,
  $ATHLETICS         ,
  $SPORT_MOTOR       ,
  $SPORT_WATER       ,

  $KIDS              ,
  $KIDS_0_5          ,
  $KIDS_6_14         ,
  $KIDS_10_16        ,
  $EDUCATIONAL       ,
  $CARTOON           ,

  $MUSIC             ,
  $ROCK_POP          ,
  $CLASSICAL         ,
  $FOLK              ,
  $JAZZ              ,
  $OPERA             ,

  $CULTURE           ,
  $PERFORMING        ,
  $FINE_ARTS         ,
  $RELIGION          ,
  $POPULAR_ART       ,
  $LITERATURE        ,
  $FILM              ,
  $EXPERIMENTAL_FILM ,
  $BROADCASTING      ,

  $SOCIAL            ,
  $MAGAZINE          ,
  $ECONOMIC          ,
  $VIP               ,

  $SCIENCE           ,
  $NATURE            ,
  $TECHNOLOGY        ,
  $MEDECINE          ,
  $FOREIGN           ,
  $SPIRITUAL         ,
  $FURTHER_EDUCATION ,
  $LANGUAGES         ,

  $HOBBIES           ,
  $TRAVEL            ,
  $HANDICRAF         ,
  $MOTORING          ,
  $FITNESS           ,
  $COOKING           ,
  $SHOPPING          ,
  $GARDENING         ,
  );

#
# This is the mapping from the source
#
my %REPLACE=(
  "Family"              => $KIDS ,
  "Movie"               => $MOVIE ,
  "News"                => $NEWS ,
  "Talk"                => $TALKSHOW ,
  );

my $PRE  = '<category lang=\"en\">' ;
my $POST = '</category>'  ;

sub myfilter {
  my ($a) = @_;
  if ( exists $REPLACE{$a} ) { # a replacement is available
    return $REPLACE{$a} ;
  } elsif ( any { /^$a$/ } @TVH_CATEGORY ) { # match default tvheadend categories, no changes required
    return $a ;
  } else {
    print STDERR "Warning: Unmanaged category: '$a'\n" ;
    return $a ;
  }
}

while (<>) {
  my $line = $_ ;
  $line =~ s/($PRE)(.*)($POST)/"$1".myfilter("$2")."$3"/ge ;
  print $line;
}

