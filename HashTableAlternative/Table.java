import java.io.*;
public class Table {

    private int nbins_;
    private MinMax[] value_ranges_;
    private Sample[][][] data_;

    public Table( final int nbins, final MinMax[] value_ranges ){
	nbins_ = nbins;
	value_ranges_ = value_ranges;
	data_ = new Sample[ nbins ][ nbins ][ nbins ];
    }

    public Table( final String filename ) throws IOException {
	load( filename );
    }

    public void load( final String filename ) throws IOException {



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
		    out.write( data_[ i ][ j ][ k ] + "_" );
		}
	    }
	}
	out.write( "\n" );

	out.close();
    }

}
