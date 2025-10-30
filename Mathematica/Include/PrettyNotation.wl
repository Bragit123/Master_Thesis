(* ::Package:: *)

BeginPackage["PrettyNotation`"];


Needs["FeynCalc`"];


(*Prettify momenta*)
MakeBoxes[p1,TraditionalForm]:=SubscriptBox["p","1"];
MakeBoxes[p2,TraditionalForm]:=SubscriptBox["p","2"];
MakeBoxes[k1,TraditionalForm]:=SubscriptBox["k","1"];
MakeBoxes[k2,TraditionalForm]:=SubscriptBox["k","2"];


(*Prettify slepton masses*)
MakeBoxes[MSf[sfermion_,2,generation_],TraditionalForm]:=SubscriptBox["m",SubscriptBox["l",ToString[generation]<> ToString[sfermion]]];


Begin["`Private`"];


End[];


EndPackage[];
