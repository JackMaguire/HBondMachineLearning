import java.io.*;
public class Table {

    private int nbins_;
    private MinMax[] value_ranges_;
    private Sample[][][] data_;

    public Table( final int nbins, final MinMax[] value_ranges ) {
	nbins_ = nbins;
	value_ranges_ = value_ranges;
	data_ = new Sample[ nbins_ ][ nbins_ ][ nbins_ ];
	for( int i=0; i<nbins_; ++i ){
	    for( int j=0; j<nbins_; ++j ){
		for( int k=0; k<nbins_; ++k ){
		    data_[ i ][ j ][ k ] = new Sample();
		}
	    }
	}
    }

    public Table( final String filename ) throws Exception {
	value_ranges_ = new MinMax[ 3 ];
	load( filename );
    }

    public void register( final double dof1, final double dof2, final double dof3, final boolean is_positive ) throws Exception{

	final int bin1 = binForValue( dof1, value_ranges_[ 0 ] );
	final int bin2 = binForValue( dof2, value_ranges_[ 1 ] );
	final int bin3 = binForValue( dof3, value_ranges_[ 2 ] );

	++data_[ bin1 ][ bin2 ][ bin3 ].num_data_points;
	if( is_positive ){
	    ++data_[ bin1 ][ bin2 ][ bin3 ].num_positive_data_points;
	}

    }

    public int binForValue( final double value, final MinMax mm ) throws Exception{
	return binForValue( value, mm, nbins_ );
    }

    public static int binForValue( final double value, final MinMax mm, final int nbins ) throws Exception{
	if( value <= mm.min ){
	    return 0;
	}
	if( value >= mm.max ){
	    return nbins - 1;
	}

	final double range = mm.max - mm.min;
	final double offset = value - mm.min;
	final double fraction = offset / range;
	final int bin = (int) ( nbins * fraction );

	if( bin < 0 ){
	    throw new Exception ( "bin is somehow: " + bin );
	}

	if( bin >= nbins )
	    return nbins - 1;
	else
	    return bin;
    }

    public void load( final String filename ) throws Exception {
	BufferedReader in = new BufferedReader( new FileReader( filename ) );

	nbins_ = Integer.parseInt( in.readLine() );

	for( int i=0; i<3; ++i ){
	    value_ranges_[ i ] = new MinMax( in.readLine() );
	}

	final String data_string = in.readLine();
	final String[] data_string_split = data_string.split( "x" );
	final long expected_length = (nbins_ * nbins_ * nbins_) + 1;
	if( data_string_split.length != expected_length ){
	    throw new Exception( "data_string_split is of length " + data_string_split.length + " instead of " + expected_length );
	}

	data_ = new Sample[ nbins_ ][ nbins_ ][ nbins_ ];
	int counter = 0;
	for( int i=0; i<nbins_; ++i ){
	    for( int j=0; j<nbins_; ++j ){
		for( int k=0; k<nbins_; ++k ){
		    data_[ i ][ j ][ k ] = new Sample( data_string_split[ counter++ ] );
		}
	    }
	}
	if( counter != expected_length - 1 ){
	    throw new Exception( "counter is equal to " + counter + " instead of " + (expected_length - 1) );
	}

	in.close();
    }

    public void save( final String filename ) throws IOException {
	BufferedWriter out = new BufferedWriter( new FileWriter( filename ) );
	
	out.write( nbins_ + "\n" );

	for ( MinMax mm : value_ranges_ ){
	    out.write( mm.toString() + "\n" );
	}

	for( int i=0; i<nbins_; ++i ){
	    for( int j=0; j<nbins_; ++j ){
		for( int k=0; k<nbins_; ++k ){
		    out.write( data_[ i ][ j ][ k ].toString() + "x" );
		}
	    }
	}
	out.write( "\n" );

	out.close();
    }

}
