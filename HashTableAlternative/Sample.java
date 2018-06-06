public class Sample {

    public long num_data_points;
    public long num_positive_data_points;

    public Sample(){
	num_data_points = 0;
	num_positive_data_points = 0;
    }

    public Sample( Sample src ){
	num_data_points = src.num_data_points;
	num_positive_data_points = src.num_positive_data_points;
    }

    public Sample( String s ){
	String[] split = s.split( "_" );
	if( split.length != 2 ){
	    throw new Exception( "Sample can not parse String: " + s );
	}
	num_data_points = Long.parseLong( split[ 0 ] );
	num_positive_data_points = Long.parseLong( split[ 1 ] );

    }

    public String toString(){
	return num_data_points + "_" + num_positive_data_points;
    }

}
