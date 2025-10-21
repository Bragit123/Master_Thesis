(* ::Package:: *)

BeginPackage["Tools`"];


Needs["FeynCalc`"];


ZSimplify::usage = "ZSimplify[amp] performs replacements to rewrite an amplitude in terms of Zql, Zqr and ZliAB instead of the sfermion mixing matrices USf."


(*Write amplitude in terms of Zql, Zqr and ZliAB instead of the sfermion mixing matrices USf.*)
ZSimplify[amp_]:=amp //
	ReplaceAll[#,{4 SMP["sin_W"]^2-3:>12 Zql}]& //
	ReplaceAll[#,{SMP["sin_W"]/SMP["cos_W"]:>3 Zqr / (SMP["sin_W"] SMP["cos_W"])}]& //
	ReplaceAll[#,{USf[2,i][A,2] Conjugate[USf[2,i][B,2]]:>KroneckerDelta[A,B]-USf[2,i][A,1] Conjugate[USf[2,i][B,1]]}]& //
	Simplify //
	ReplaceAll[#,{2SMP["sin_W"]^2 KroneckerDelta[A,B]-USf[2,i][A,1] Conjugate[USf[2,i][B,1]]->-2 ZliAB}]&


Begin["`Private`"];


End[];


EndPackage[];
