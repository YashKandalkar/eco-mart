
<?php

$database = "BLUDB";        # Get these database details from
$hostname = "db2w-ggsmzuf.uk-south.db2w.cloud.ibm.com";  # the web console
$user     = "bluadmin";   #
$password = "8FxMb34HHWOVAzhzKs8kL15@_MTi4";   #
// $port     = 50000;          #
$ssl_port = 50001;          #

# Build the connection string
#
$driver  = "DRIVER={IBM DB2 ODBC DRIVER};";
// $dsn     = "DATABASE=$database; " .
//            "HOSTNAME=$hostname;" .
//            "PORT=$port; " .
//            "PROTOCOL=TCPIP; " .
//            "UID=$user;" .
//            "PWD=$password;";
$ssl_dsn = "DATABASE=$database; " .
           "HOSTNAME=$hostname;" .
           "PORT=$ssl_port; " .
           "PROTOCOL=TCPIP; " .
           "UID=$user;" .
           "PWD=$password;" .
           "SECURITY=SSL;";
// $conn_string = $driver . $dsn;     # Non-SSL
$conn_string = $driver . $ssl_dsn; # SSL

# Connect
#
$conn = odbc_connect( $conn_string, "bluadmin", "8FxMb34HHWOVAzhzKs8kL15@_MTi4" );
if( $conn )
{
    echo "Connection succeeded.";

    # Disconnect
    #
    odbc_close( $conn );
}
else
{
    echo "Connection failed.";
}
?>