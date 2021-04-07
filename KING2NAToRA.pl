use strict;
use Getopt::Long;
use Data::Dumper;

my ($help, $input, $output, $help, $kinship);
my (@split);

GetOptions (
	"help!"=>\$help,
	"input=s"=>\$input,
	"output=s"=>\$output,
)or die(apresentaAjuda());

if($help or $input eq "" or $output eq ""){
	apresentaAjuda();
}

open(IF, $input) or die("Error: the input file ($input) was not found\n");
open(OF, ">$output");

my $cabecalho=1;

while(<IF>){
	if($cabecalho==0){
		@split=split(/\s+/,$_);
# 		print Dumper @split;
# 		<STDIN>;
		#print "==@split[0]==\n";
		$kinship=@split[7];
		#$kinship=(@split[8]/4)+(@split[9]/2);
		print OF @split[1]."\t".@split[3]."\t".$kinship."\n";
	}else{
		$cabecalho=0;
	}
}


sub apresentaAjuda(){
  print "\n";
  print "=========================================================================================\n";
  print "**											**\n";
  print "**											**\n";
  print "** Opcoes:										**\n";
  print "**											**\n";
  print "**	-input <Input file>		Input file from KING (.kin file)	 	**\n";
  print "**											**\n";
  print "**	-output <Output file>		Name of output file				**\n";
  print "**											**\n";
  print "=========================================================================================\n";
  die("\n");

}
