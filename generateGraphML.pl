use strict;
use Getopt::Long;
use Data::Dumper;
use threads;
use threads::shared;

#use constant limite => 40000;
#GetOptions

our ($help, $split, $corte, $lista, $input, $output, $reap, $plink, $default, $rel, $color, $format);
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
	"color=s"=>\$color,
	"format=s"=>\$format,
	"help!"=>\$help,
	"rel!"=>\$rel,
)or die(apresentaAjuda());

if($help or $input eq "" or ($plink eq "" && $reap eq "" && $default eq "")){	#Se o usuario pedir ajuda ou algum dos arquivos nao forem setados
	apresentaAjuda();							#apresente ajuda
}

if($color eq ""){
	$color= "#3999dc";
}else{
	$color= "#".$color;
}


abreArquivoInput();
if($lista ne ""){
	leArquivoDeEliminar();
}
geraXGMML();

sub geraXGMML{
	my($i, $j, $label, $label2, $weight, $id1, $id2);
	my(@keysLVL1, @keysLVL2, @temp);
	
	open (OF, ">$output\.graphml");

	@keysLVL1=keys(%label);
	
	print OF "<graphml
 xmlns=\"http://graphml.graphdrawing.org/xmlns\"
 xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"
 xmlns:y=\"http://www.yworks.com/xml/graphml\"
 xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.0/ygraphml.xsd\">\n";
	
	print OF "  <key id=\"d0\" for=\"node\" yfiles.type=\"nodegraphics\"/>\n";
	print OF "  <key id=\"d1\" for=\"node\" attr.type=\"string\" attr.name=\"color\"/>\n";
	print OF "  <key id=\"d2\" for=\"edge\" attr.type=\"double\" attr.name=\"weight\"/>\n";
	print OF "  <graph id=\"G\" edgedefault=\"undirected\">\n";
	if (!$split){
		foreach $i (0..$#keysLVL1){
			if($lista eq ""){
				#Maybe add family atribute
				printNode($label{@keysLVL1[$i]},@keysLVL1[$i],$format, $color);
				
			}else{
				if(!exists ($eliminar{@keysLVL1[$i]})){
					printNode($label{@keysLVL1[$i]}, @keysLVL1[$i], $format, $color);
				}
			}
		}
		
		@keysLVL1=keys(%hash);
		foreach $i (0..$#keysLVL1){
			@keysLVL2=keys(%{$hash{@keysLVL1[$i]}});
			foreach $j (0..$#keysLVL2){
			
				$id1= $label{@keysLVL1[$i]};
				$id2= $label{@keysLVL2[$j]};
				$weight= $hash{@keysLVL1[$i]}{@keysLVL2[$j]};
				if($lista eq ""){
					if($corte eq ""){
						printEdge($id1, $id2,@keysLVL1[$i],@keysLVL2[$j], $weight);
					}else{
						if($hash{@keysLVL1[$i]}{@keysLVL2[$j]}> $corte){
							printEdge($id1, $id2,@keysLVL1[$i],@keysLVL2[$j], $weight);
						}
					}
				}else{
					if(!exists ($eliminar{@keysLVL1[$i]}) && !exists ($eliminar{@keysLVL2[$j]})){
						if($corte eq ""){
							printEdge($id1, $id2,@keysLVL1[$i],@keysLVL2[$j], $weight);
						}else{
							if($hash{@keysLVL1[$i]}{@keysLVL2[$j]}> $corte){
								printEdge($id1, $id2,@keysLVL1[$i],@keysLVL2[$j], $weight);
							}
						}
					}
				}
			}
		
		}
		
	}else{
		foreach $i (0..$#keysLVL1){
			@temp=split("_", @keysLVL1[$i]);
			$label= @temp[$#temp];
			if($lista eq ""){
				printNode($label{@keysLVL1[$i]},$label,$format, $color);
			}else{
				if(!exists ($eliminar{@keysLVL1[$i]})){
					printNode($label{@keysLVL1[$i]},$label,$format, $color);
				}
			}
		}
		
		@keysLVL1=keys(%hash);
		foreach $i (0..$#keysLVL1){
			@temp=split("_", @keysLVL1[$i]);
			$label= @temp[$#temp];
			
			@keysLVL2=keys(%{$hash{@keysLVL1[$i]}});
			foreach $j (0..$#keysLVL2){
				
				@temp=split("_", @keysLVL2[$j]);
				$label2= @temp[$#temp];
				
				$id1= $label{@keysLVL1[$i]};
				$id2= $label{@keysLVL2[$j]};
				$weight= $hash{@keysLVL1[$i]}{@keysLVL2[$j]};
				
				if($lista eq ""){
					if($corte eq ""){
						printEdge($id1, $id2,$label,$label2, $weight);
					}else{
						if($hash{@keysLVL1[$i]}{@keysLVL2[$j]}> $corte){
							printEdge($id1, $id2,$label,$label2, $weight);
						}
					}
				}else{
					if(!exists ($eliminar{@keysLVL1[$i]}) && !exists ($eliminar{@keysLVL2[$j]})){
						if($corte eq ""){
							printEdge($id1, $id2,$label,$label2, $weight);
						}else{
							if($hash{@keysLVL1[$i]}{@keysLVL2[$j]}> $corte){
								printEdge($id1, $id2,$label,$label2, $weight);
							}
						}
					}
				}
			}
		
		}
	
	}
	print OF "  </graph>
</graphml>";

}

sub printNode{
	my $id=@_[0];
	my $labelNode=@_[1];
	my $format= @_[2];

	print OF "      <node id=\"$id\">
      <data key=\"d0\">
        <y:ShapeNode>
          <y:Fill color=\"$color\" transparent=\"false\"/>
          <y:NodeLabel>$labelNode</y:NodeLabel>
        </y:ShapeNode>
      </data>
    </node>\n";
	
}

sub printEdge{
	my $id1=@_[0];
	my $id2=@_[1];
	my $labelNode1=@_[2];
	my $labelNode2=@_[3];
	my $weight= @_[4];

	print OF "    <edge id=\"$labelNode1-$labelNode2\" source=\"$id1\" target=\"$id2\">
      <data key=\"d2\">$weight</data>
    </edge>\n";
	
}

sub leArquivoDeEliminar(){
	my(@arquivo, @temp);
	my ($i, $id);
	
	open (IF, $lista) or die ("Erro: arquivo $lista nao encontrado\n");
	@arquivo=<IF>;
	
	
	
	foreach $i (0..$#arquivo){
		@arquivo[$i]=~ s/\n//gi; 
		@arquivo[$i]=~ s/\r//gi; 
		
		$id=@arquivo[$i];
		
		if($rel){
			my @split=split(/\s+/, @arquivo[$i]);
			$id= @split[1];
		}
		
		$eliminar{$id}=1;
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
  print "**	-color				Seleciona a cor (use hexcode sem o #)	**\n";
  print "**				Ex: se interessado na cor #0000ff escreva 0000ff	**\n";
  print "**	-split					quebrar ID por _ pra diminuir o label	**\n";
 print "**	-h					Mostra essa mensagem			**\n";
  print "**											**\n";
  print "==========================================================================================\n";
  die("\n");
} 

