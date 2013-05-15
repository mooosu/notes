create_lock(){
    watched_dir=$1
    lock_file=`echo "/tmp/watching_$watched_dir.lock" | sed -e 's/\//_/g'` 
    echo "lock:$lock_file"
    if [ -f $lock_file ] ; then
        exit 1
    fi
    echo $watched_dir > $lock_file 
}
escape_dirs(){
    dirs=$1
    new_dirs=
    for line in $lines
    do
        dir=`echo $line | sed -e 's/\//\\\\\//g'`
        new_dirs="$new_dirs $dir"
    done
    echo $new_dirs
}
extract_dest_dir(){
    escaped=$1
    dir=$2
    for i in $escaped
    do
        if [ -n "`echo $dir | grep $i`" ];then
            dest_dir=`echo ${dir} | sed -e "s/$i\/*//g"`
            break
        fi
    done
    echo $dest_dir
}

lines=`cat $1 | awk '{print length, $0}' | sort -rn | sed -e 's/^[0-9 ]\+//g' | sed -e 's/\/$//g'`
escaped=$(escape_dirs $lines)


/usr/bin/inotifywait -mrq --timefmt '%Y-%m-%dT%H:%M' --format '%T %e %w %f' -e close_write,delete,create,attrib --fromfile $1 | while read datetime event dir file
do
    echo "date: $datetime,event:$event,file:$file,dir:$dir"
    is_dir=`echo $event | grep 'ISDIR'`
    dest_dir=$(extract_dest_dir "$escaped" $dir)
    if [ -z "$is_dir" ]; then
        rsync -rv $dir$file rsync_dest/$dest_dir$file
    else
        rsync -rv $dir$file rsync_dest/$dest_dir
    fi
done
