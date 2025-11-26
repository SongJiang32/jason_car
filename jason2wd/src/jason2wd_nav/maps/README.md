# SAVE MAP WHEN YOU BUILD A MAP
$ rosrun map_server map_saver -f <mapname>
then you will see "<mapname>.png" and "<mapname>.yaml"

# OPEN THE MAP EXITED, THE DEFAULT TOPIC IS MAP(you can open rviz to view)
$ rosrun map_server map_server <mapname>.yaml
