import java.io.*;

public final class EvaluateTable {

    public static void main( String[] args ) throws Exception{

	//args:
	//0: table
	//1-N: data files

	final Table t = new Table( args[ 0 ] );

	final ResultBundle[] result_bundles = new ResultBundle[ args.length - 1 ];

	for( int i=1; i<args.length; ++i ){
	    result_bundles[ i-1 ] = new ResultBundle();

	    final String filename = args[ i ];
	    final BufferedReader in = new BufferedReader( new FileReader( filename ) );
	    for( String line = in.readLine(); line != null; line = in.readLine() ){
		evaluateLine( result_bundles[ i-1 ], t, line );
	    }
	    in.close();
	}

	double min = 1.0;
	String title = "";
	String out = "";
	for( ResultBundle rb : result_bundles ){
	    final double ppv = rb.ppv();
	    final double npv = rb.npv();
	    if( ppv < min ) min = ppv;
	    if( npv < min ) min = npv;
	    title += "ppv\tnpv\t";
	    out += ppv + "\t" + npv + "\t";
	}
	title += "min";
	out += min;
	System.out.println( title );
	System.out.println( out );
    }

    public static void evaluateLine( final ResultBundle results, final Table t, final String line ) throws Exception{
	evaluateLine( results, t, line, 0.01 );
    }

    public static void evaluateLine( final ResultBundle results, final Table t, final String line, final double threshold ) throws Exception{
	final String[] split = line.split( "," );
	if( split.length != 11 ){
	    //System.err.println( "split.length != 11, == " + split.length );
	    //System.err.println( filename );
	    System.err.println( line );
	    throw new Exception( "split.length != 11, == " + split.length );
	}

	final double dof1 = Double.parseDouble( split[ 8 ] );
	final double dof2 = Double.parseDouble( split[ 9 ] );
	final double dof3 = Double.parseDouble( split[ 10 ] );

	final double hbond_score = Double.parseDouble( split[ 0 ] );
	final boolean is_positive = hbond_score < -0.25;//split between 0 and -0.5. Not expecting to get anything near this line


	final Sample sample = t.getSample( dof1, dof2, dof3 );
	boolean hbond_predicted = false;
	if( sample.num_data_points == 0 ){
	    hbond_predicted = true;//?
	} else {
	    final double frac = sample.num_positive_data_points / ((double)sample.num_data_points);
	    hbond_predicted = frac > threshold;
	}

	if( is_positive ){
	    ++results.ppv_denom;
	    if( hbond_predicted ) ++results.ppv_numer;
	} else {
	    ++results.npv_denom;
	    if( ! hbond_predicted ) ++results.npv_numer;
	}
    }

    private final static class ResultBundle {
	public int ppv_numer = 0;
	public int ppv_denom = 0;
	public int npv_numer = 0;
	public int npv_denom = 0;

	public double ppv(){
	    if( ppv_denom == 0 ) return 0;
	    return ((double) ppv_numer)/ ((double) ppv_denom);
	}

	public double npv(){
	    if( npv_denom == 0 ) return 0;
	    return ((double) npv_numer)/ ((double) npv_denom);
	}

    }

}
