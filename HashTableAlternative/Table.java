import java.io.*;
public class Table {

    private int nbins_;
    private Sample[][][] data_;
    private MinMax[] value_ranges_;

    public Table( final int nbins, final MinMax[] value_ranges ){
	nbins_ = nbins;
	data_ = new Sample[ nbins ][ nbins ][ nbins ];
	value_ranges_ = value_ranges;
    }

    public Table( final String filename ) throws IOException {
	load( filename );
    }

    public void load( final String filename ) throws IOException {

    }

    public void save( final String filename ) throws IOException {
	BufferedWriter out = new BufferedWriter( new FileWriter( filename ) );
	
	out.write( nbins_ + "\n" );

	
	//out.write( + "\n" );

	out.close();
    }

}
