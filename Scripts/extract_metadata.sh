#!/bin/bash

# Arquivo de saída CSV
output_csv="metadata.csv"

# Cabeçalho do arquivo CSV
echo "Nome do Arquivo,Tamanho (bytes),Duração (segundos),Bitrate do Áudio (kbps)" > "$output_csv"

# Ler cada linha do arquivo file_list.txt
while IFS= read -r line; do
  # Extrair o nome do arquivo da linha
  file=$(echo $line | sed "s/file '\(.*\)'/\1/")
  
  # Verificar se o arquivo existe
  if [[ -f "$file" ]]; then
    # Extrair metadados usando ffprobe
    size=$(stat -c%s "$file")
    duration=$(ffprobe -v error -select_streams v:0 -show_entries format=duration -of csv=p=0 "$file")
    audio_bitrate=$(ffprobe -v error -select_streams a:0 -show_entries stream=bit_rate -of csv=p=0 "$file" | awk '{print $1/1000}')
    
    # Adicionar as informações ao arquivo CSV
    echo "$file,$size,$duration,$audio_bitrate" >> "$output_csv"
  else
    echo "Arquivo não encontrado: $file"
  fi
done < file_list.txt

echo "Metadados extraídos com sucesso para $output_csv"
