subjects=/data/jux/BBL/studies/reward/rawData/*/*/; 

for s in $subjects; 
do id=$(echo $s|cut -d'/' -f7); 
tp=$(echo $s|cut -d'/' -f8); 
sc=$(echo $tp|cut -d'x' -f2); 
da=$(echo $tp|cut -d'x' -f1); 
echo ${id},${tp},${da},${sc}>> cheadRewardDicoms_09-24-2018.csv; done

