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

open(IF, $input) or die("Erro: $input não encontrado");
open(OF, ">$output");

while(<IF>){
	@split=split(/\s+/,$_);
	$kinship=(@split[6]/4)+(@split[7]/2);
	print OF @split[1]."\t".@split[3]."\t".$kinship."\n";
}


sub apresentaAjuda(){
  print "\n";
  print "=========================================================================================\n";
  print "**											**\n";
  print "**											**\n";
  print "** Opcoes:										**\n";
  print "**											**\n";
  print "**	-input <Nome do arquivo>		Arquivo com o resultado do .genome 	**\n";
  print "**											**\n";
  print "**	-output <Nome do arquivo>		Nome do arquivo de saída		**\n";
  print "**											**\n";
  print "=========================================================================================\n";
  die("\n");
} 