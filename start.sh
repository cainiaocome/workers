#!/usr/bin/env sh

case "$1" in
    start)
        nohup ./text_index.py >log.index 2>&1 &
        nohup ./simdht_worker.py >log 2>&1 &
    ;;
    stop)
        pid_text_index=`ps aux | grep text_index | grep -v grep | awk '{print $2}'`
        kill 9 $pid_text_index
        pid_simdht_worker=`ps aux | grep simdht_worker | grep -v grep | awk '{print $2}'`
        kill 9 $pid_simdht_worker
    ;;
    *)
        echo "Usage: ./start.sh start|stop"
    ;;
esac
