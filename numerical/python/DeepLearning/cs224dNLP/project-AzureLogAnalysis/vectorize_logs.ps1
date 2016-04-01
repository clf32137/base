#########################
##Run when on windows
#########################
$vectorDimLen = 200
$contectSize = 100
$finalTextVecsPath = ".\data\agentlogs_final.txt"

#If the final vectors file doesn't exist, recreate it.
if(!(Test-Path $finalTextVecsPath))
{
	dir .\data\* -include *.log -rec | gc | out-file .\data\all_logs_unicode.txt
	Write-Host "Finished combining files";
	gc -en Unicode .\data\all_logs_unicode.txt | Out-File -en ascii .\data\all_logs_ascii.txt
	Write-Host "Finished converting to ascii";
}

python processAzureAgentLogs.py
Write-Host "Finished removing guids etc.";

./word2vec -train data/agentlogs_final.txt -output data/agentlogs.bin -cbow 1 -size $vectorDimLen -window $contectSize -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15
Write-Host "Finished training word vectors";

./readbin data/agentlogs.bin > data/agentlogsVecs.txt
Write-Host "Finished converting bin vectors file to txt";

gc -en Unicode .\data\agentlogsVecs.txt | Out-File -en ascii .\data\agentlogsVecsAscii.txt

python plotTxtVectors.py $vectorDimLen "data\agentlogsVecsAscii.txt" "successfully" "__VHD__"

