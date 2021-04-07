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

my $cabecalho=1;

while(<IF>){
	if($cabecalho==0){
		@split=split(/\s+/,$_);
# 		print Dumper @split;
# 		<STDIN>;
		$kinship=(@split[8]/4)+(@split[9]/2);
		print OF @split[2]."\t".@split[4]."\t".$kinship."\n";
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
  print "**	-input <Nome do arquivo>		Arquivo com o resultado do .genome 	**\n";
  print "**											**\n";
  print "**	-output <Nome do arquivo>		Nome do arquivo de saída		**\n";
  print "**											**\n";
  print "=========================================================================================\n";
  die("\n");
} 