public class MinMax {
    public double min;
    public double max;

    public MinMax(){
	min = 99999;
	max = -99999;
    }

    public MinMax( final MinMax src ){
	min = src.min;
	max = src.max;
    }

    public MinMax( final double min_val, final double max_val ){
	min = min_val;
	max = max_val;
    }

    public MinMax( String s ) throws Exception{
	String[] split = s.split( "_" );
	if( split.length != 2 ){
	    throw new Exception( "MinMax can not parse String: " + s );
	}
	min = Double.parseDouble( split[ 0 ] );
	max = Double.parseDouble( split[ 1 ] );
    }

    public String toString(){
	return min + "_" + max;
    }
}
