use strict;
use Getopt::Long;
use Data::Dumper;
use threads;
use threads::shared;

#use constant limite => 40000;
#GetOptions

our ($help, $split, $corte, $lista, $input, $output, $reap, $plink, $default);
our (%hash, %eliminar, %label);

GetOptions (
	"corte=s"=>\$corte,
	"lista=s"=>\$lista,
	"input=s"=>\$input,
	"output=s"=>\$output,
	"plink"=>\$plink,
	"split"=>\$split,
	"reap"=>\$reap,
	"default"=>\$default,
	"help!"=>\$help,
)or die(apresentaAjuda());

if($help or $input eq "" or ($plink eq "" && $reap eq "" && $default eq "")){	#Se o usuario pedir ajuda ou algum dos arquivos nao forem setados
	apresentaAjuda();							#apresente ajuda
}


abreArquivoInput();
if($lista ne ""){
	leArquivoDeEliminar();
}
geraGML();

sub geraGML{
	my($i, $j, $label);
	my(@keysLVL1, @keysLVL2, @temp);
	
	open (OF, ">$output");
	
	@keysLVL1=keys(%label);
	
	if (!$split){
		
		print OF "graph [\n";
		print OF "	directed 0\n";
		foreach $i (0..$#keysLVL1){
			if($lista eq ""){
				print OF "	node [\n";
				print OF "		id ".$label{@keysLVL1[$i]} ."\n";
				print OF "		label \"@keysLVL1[$i]\"\n";
				print OF "	]\n";
			}else{
				if(!exists ($eliminar{@keysLVL1[$i]})){
					print OF "	node [\n";
					print OF "		id ".$label{@keysLVL1[$i]} ."\n";
					print OF "		label \"@keysLVL1[$i]\"\n";
					print OF "	]\n";
				}
			}
		}
		
		@keysLVL1=keys(%hash);
		foreach $i (0..$#keysLVL1){
			@keysLVL2=keys(%{$hash{@keysLVL1[$i]}});
			foreach $j (0..$#keysLVL2){
				if($lista eq ""){
					if($corte eq ""){
						print OF "	edge [\n";
						print OF "		source ".$label{@keysLVL1[$i]}."\n";
						print OF "		target ".$label{@keysLVL2[$j]}."\n";
						print OF "		label \"".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\"\n";
						print OF "		weight ".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\n";
						print OF "	]\n";
					}else{
						if($hash{@keysLVL1[$i]}{@keysLVL2[$j]}> $corte){
							print OF "	edge [\n";
							print OF "		source ".$label{@keysLVL1[$i]}."\n";
							print OF "		target ".$label{@keysLVL2[$j]}."\n";
							print OF "		label \"".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\"\n";
							print OF "		weight ".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\n";
							print OF "	]\n";
						}
					}
				}else{
					if(!exists ($eliminar{@keysLVL1[$i]}) && !exists ($eliminar{@keysLVL2[$j]})){
						if($corte eq ""){
							print OF "	edge [\n";
							print OF "		source ".$label{@keysLVL1[$i]}."\n";
							print OF "		target ".$label{@keysLVL2[$j]}."\n";
							print OF "		label \"".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\"\n";
							print OF "		weight ".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\n";
							print OF "	]\n";
						}else{
							if($hash{@keysLVL1[$i]}{@keysLVL2[$j]}> $corte){
								print OF "	edge [\n";
								print OF "		source ".$label{@keysLVL1[$i]}."\n";
								print OF "		target ".$label{@keysLVL2[$j]}."\n";
								print OF "		label \"".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\"\n";
								print OF "		weight ".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\n";
								print OF "	]\n";
							}
						}
					}
				}
			}
		
		}
		print OF "]\n";
	}else{
		print OF "graph [\n";
		print OF "	directed 0\n";
		foreach $i (0..$#keysLVL1){
			@temp=split("_", @keysLVL1[$i]);
			$label= @temp[$#temp];
			if($lista eq ""){
				print OF "	node [\n";
				print OF "		id ".$label{@keysLVL1[$i]} ."\n";
				print OF "		label \"$label\"\n";
				print OF "	]\n";
			}else{
				if(!exists ($eliminar{@keysLVL1[$i]})){
					print OF "	node [\n";
					print OF "		id ".$label{@keysLVL1[$i]} ."\n";
					print OF "		label \"$label\"\n";
					print OF "	]\n";
				}
			}
		}
		
		@keysLVL1=keys(%hash);
		foreach $i (0..$#keysLVL1){
			@keysLVL2=keys(%{$hash{@keysLVL1[$i]}});
			foreach $j (0..$#keysLVL2){
				if($lista eq ""){
					if($corte eq ""){
						print OF "	edge [\n";
						print OF "		source ".$label{@keysLVL1[$i]}."\n";
						print OF "		target ".$label{@keysLVL2[$j]}."\n";
						print OF "		label \"".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\"\n";
						print OF "		weight ".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\n";
						print OF "	]\n";
					}else{
						if($hash{@keysLVL1[$i]}{@keysLVL2[$j]}> $corte){
							print OF "	edge [\n";
							print OF "		source ".$label{@keysLVL1[$i]}."\n";
							print OF "		target ".$label{@keysLVL2[$j]}."\n";
							print OF "		label \"".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\"\n";
							print OF "		weight ".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\n";
							print OF "	]\n";
						}
					}
				}else{
					if(!exists ($eliminar{@keysLVL1[$i]}) && !exists ($eliminar{@keysLVL2[$j]})){
						if($corte eq ""){
							print OF "	edge [\n";
							print OF "		source ".$label{@keysLVL1[$i]}."\n";
							print OF "		target ".$label{@keysLVL2[$j]}."\n";
							print OF "		label \"".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\"\n";
							print OF "		weight ".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\n";
							print OF "	]\n";
						}else{
							if($hash{@keysLVL1[$i]}{@keysLVL2[$j]}> $corte){
								print OF "	edge [\n";
								print OF "		source ".$label{@keysLVL1[$i]}."\n";
								print OF "		target ".$label{@keysLVL2[$j]}."\n";
								print OF "		label \"".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\"\n";
								print OF "		weight ".$hash{@keysLVL1[$i]}{@keysLVL2[$j]}."\n";
								print OF "	]\n";
							}
						}
					}
				}
			}
		
		}
		print OF "]\n";
	
	}

}

sub leArquivoDeEliminar(){
	my(@arquivo, @temp);
	my ($i);
	
	open (IF, $lista) or die ("Erro: arquivo $lista nao encontrado\n");
	@arquivo=<IF>;
	
	foreach $i (0..$#arquivo){
		@arquivo[$i]=~ s/\n//gi; 
		@arquivo[$i]=~ s/\r//gi; 
		
		$eliminar{@arquivo[$i]}=1;
	}
}

sub abreArquivoInput(){
	my(@arquivo, @temp);
	my ($i, $contador);
	
	open (IF, $input) or die ("Erro: arquivo $input nao encontrado\n");
	@arquivo=<IF>;
	if($plink){
		foreach $i (1..$#arquivo){
			@temp=split(" ", @arquivo[$i]);
			
			$hash{@temp[1]}{@temp[3]}=@temp[7]/4+@temp[8]/2;
			#if($hash{@temp[1]}{@temp[3]} > $corte){
				#print "@temp[7] div 4+@temp[8] div 2";
				#print Dumper @temp;
				#<STDIN>;
			#}
			if(!exists($label{@temp[1]})){
				$contador++;
				$label{@temp[1]}=$contador;
			}
			if(!exists($label{@temp[3]})){
				$contador++;
				$label{@temp[3]}=$contador;
			}
		}
	}else{
		if($reap){
			foreach $i (0..$#arquivo){
				@temp=split(" ", @arquivo[$i]);
				
				$hash{@temp[1]}{@temp[3]}=@temp[6]/4+@temp[7]/2;
				#if($hash{@temp[1]}{@temp[3]} > $corte){
					#print "@temp[7] div 4+@temp[8] div 2";
					#print Dumper @temp;
					#<STDIN>;
				#}
				if(!exists($label{@temp[1]})){
					$contador++;
					$label{@temp[1]}=$contador;
				}
				if(!exists($label{@temp[3]})){
					$contador++;
					$label{@temp[3]}=$contador;
				}
			}
		}else{
			if($default){
				foreach $i (0..$#arquivo){
					@arquivo[$i]=~ s/\n//gi;
					@arquivo[$i]=~ s/\r//gi;
					@temp=split("\t", @arquivo[$i]);
					
					#print "@temp[0] e @temp[1]\n";
					if(@temp[0] ne @temp[1]){
						$hash{@temp[0]}{@temp[1]}=@temp[2];
					}
					#print "@temp[0] @temp[1] @temp[2]\n";
					#if($hash{@temp[1]}{@temp[3]} > $corte){
						#print "@temp[7] div 4+@temp[8] div 2";
						#print Dumper @temp;
						#<STDIN>;
					#}
					
					
					if(!exists($label{@temp[0]})){
						$contador++;
						$label{@temp[0]}=$contador;
					}
					if(!exists($label{@temp[1]})){
						$contador++;
						$label{@temp[1]}=$contador;
					}
				}
			}
		}
	}
	
}




sub apresentaAjuda(){
  print "\n";
  print "==========================================================================================\n";
  print "**											**\n";
  print "**											**\n";
  print "** Opcoes:										**\n";
  print "**											**\n";
  print "**	-corte					Valor de corte				**\n";
  print "**	-lista					Lista dos eliminados			**\n";
  print "**	-input					Matriz de parentesco			**\n";
  print "**	-output					Nome do GML de output			**\n";
  print "**	-plink					Sinaliza que é arquivo do Plink		**\n";
  print "**	-reap					Sinaliza que é arquivo do REAP		**\n";
  print "**	-default				Sinaliza que é arquivo default		**\n";
  print "**	-split					quebrar ID por _ pra diminuir o label	**\n";
 print "**	-h					Mostra essa mensagem			**\n";
  print "**											**\n";
  print "==========================================================================================\n";
  die("\n");
} 
