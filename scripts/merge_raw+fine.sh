#!/bin/bash

# TODO: option to delete the jpegs that hve been injected into the nef
# TODO: option to make a backup of the nef before overwriting (.nef~)

CWP=$(pwd)

if [ $# -lt 2 ];
then
	printf "Usage: %s raw_dir fine_dir\n" $0 
	exit 1
fi

raw_dir="$1"
fine_dir="$2"

if [ ! -d "$raw_dir" ]; 
then
	printf "%s is not a directory\n" "$raw_dir" 
	exit 2
fi 

if [ ! -d "$fine_dir" ]; 
then
	printf "%s is not a directory\n" "$fine_dir" 
	exit 3
fi

[[ "$raw_dir" != */ ]] && raw_dir="$raw_dir/"
[[ "$fine_dir" != */ ]] && fine_dir="$fine_dir/"

# printf "[%s] [%s]\n" "$raw_dir" "$fine_dir"

TEMP_NEF=/tmp/tmp.nef
TEMP_JPEG=/tmp/tmp.jpeg
JPG_LIST=/tmp/jpg_list.tmp

cd "$fine_dir"

# find all jpegs in relative path from $fine_dir 
find ./ -iregex '.*\.jpe?g' > $JPG_LIST

cd "$CWP"

cat $JPG_LIST | while read input_jpeg; 
do
	path_to_nef="${input_jpeg%/*}"
	name_of_nef="${input_jpeg##*/}"
	name_of_nef="${name_of_nef%.*}"
	
	# printf "[%s] [%s] [%s]\n" "$input_jpeg" "$path_to_nef" "$name_of_nef"
	
	# find a potential nef file to process in a case insensitive way
	target_nef=$(find "$raw_dir$path_to_nef/" -maxdepth 1 -iname "$name_of_nef.nef" 2>/dev/null)
	
	if [[ -n "$target_nef" && "$(echo $target_nef | wc -l)" -eq 1 ]];
	then
		if [ -w "$target_nef" ];
		then
			jpegtran -optimize -copy none -outfile $TEMP_JPEG "$fine_dir$input_jpeg"
			nef-cli -i "$target_nef" -p $TEMP_JPEG -o $TEMP_NEF
			touch -r "$target_nef" $TEMP_NEF
			printf "Injecting [%s] into [%s]\n" "$fine_dir$input_jpeg" "$target_nef" | sed -e 's:/\./:/:g'
			mv $TEMP_NEF "$target_nef"
		else
			printf "WARNING: [%s] found to match [%s], but is not writable\n" "$target_nef" "$fine_dir$input_jpeg" | sed -e 's:/\./:/:g' 1>&2
		fi
	else
		printf "WARNING: no nef found to match [%s]\n" "$fine_dir$input_jpeg" | sed -e 's:/\./:/:g' 1>&2
	fi
done;

rm $TEMP_NEF 2>/dev/null
rm $TEMP_JPEG 2>/dev/null
rm $JPG_LIST 2>/dev/null
