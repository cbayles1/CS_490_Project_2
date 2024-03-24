#downloading all .bed.gz files given by the user, and putting them in ~/data/bed/positives
while true
do
    read -p "Enter a download URL or DONE to finish: " url
    if [ "$url" = DONE ]; then
        break
    else
        wget $url -P ~/data/bed/positives
    fi
done

#unzipping all .bed.gz files in ~/data/bed/positives
cd ~/data/bed/positives
for file in *.bed.gz
do
    gunzip "$file"
done

#converting positive bed files to negative bed files
#then converting both bed files to atgc, and moving them to ~/data/atgc/
i=1
for file in *.bed
do
    echo $file
    chmod 755 $file
    refPath=/proj/SIUE-CS590-490/reference/hg38.fa
    outPositivesDir=~/data/atgc/positives
    outNegativesDir=~/data/atgc/negatives
    outPositivesPath=$outPositivesDir/$i.txt
    outNegativesPath=$outNegativesDir/$i.txt
    mkdir -p $outPositivesDir
    mkdir -p $outNegativesDir
    touch $outPositivesPath
    touch $outNegativesPath

    python /users/cbayles/createNegativeBed.py $file /users/cbayles/data/bed/positives/ /users/cbayles/data/bed/negatives/

    bedtools getfasta -fi $refPath -bed ~/data/bed/positives/$file -fo $outPositivesPath > /dev/null
    bedtools getfasta -fi $refPath -bed ~/data/bed/negatives/$file -fo $outNegativesPath > /dev/null
    
    i=$(($i + 1))
done