import java.io.*;

public class CreateTable {

    /*
      0,249.336,-0.854788,0.950156,-3.58892,-0.907735,-0.0685858,1.28586,1.83715,2.18063,3.8097
      0,1      ,2        ,3       ,4       ,5        ,6         ,7      ,8      ,9      ,10
     */

    public static void main(String[] args) throws Exception{
	
	//Args:
	//0 comma-separated list of input csv files
	//1 output file
	//2 number of bins per DOF

	if( args.length < 3 ){
	    System.err.println( "Arguments:" );
	    System.err.println( "1: comma-separated list of input csv files" );
	    System.err.println( "2: output file" );
	    System.err.println( "3: number of bins per DOF" );
	    System.exit( 1 );
	}

	final String[] input_files = args[ 0 ].split( "," );
	final String output_File = args[ 1 ];
	final int nbins = Integer.parseInt( args[ 2 ] );

	MinMax[] value_ranges = new MinMax[ 3 ];
	value_ranges[ 0 ] = get_min_and_max_for_column( 8, input_files );
	value_ranges[ 1 ] = get_min_and_max_for_column( 9, input_files );
	value_ranges[ 2 ] = get_min_and_max_for_column( 10, input_files );

	Table t = new Table( nbins, value_ranges );

    }

    public static void populate_table( final Table t, final String[] input_files ){
	for( String filename : input_files ){
	    final BufferedReader in = new BufferedReader( new FileReader( filename ) );
	    for( String line = in.readLine(); line != null; line = in.readLine() ){
		final String[] split = line.split( "," );
		if( split.length != 11 ){
		    //System.err.println( "split.length != 11, == " + split.length );
		    System.err.println( filename );
		    System.err.println( line );
		    throw new Exception( "split.length != 11, == " + split.length );
		}

		final double dof1 = Double.parseDouble( split[ 8 ] );
		final double dof2 = Double.parseDouble( split[ 9 ] );
		final double dof3 = Double.parseDouble( split[ 10 ] );

		final double hbond_score = Double.parseDouble( split[ 0 ] );
		final boolean is_positive = hbond_score < -0.25;//split between 0 and -0.5. Not expecting to get anything near this line

		t.register( dof1, dof2, dof3, is_positive );
	    }
	    in.close();
	}
    }

    public static MinMax get_min_and_max_for_column( final int zero_indexed_col_no, final String[] filenames ) throws IOException{

	final MinMax mm = new MinMax();

	for( String filename : filenames ){
	    final BufferedReader in = new BufferedReader( new FileReader( filename ) );
	    for( String line = in.readLine(); line != null; line = in.readLine() ){
		final String[] split = line.split( "," );
		if( split.length != 11 ){
		    System.err.println( "split.length != 11, == " + split.length );
		    System.err.println( filename );
		    System.err.println( line );
		    System.exit( 1 );
		}

		final double value = Double.parseDouble( split[ zero_indexed_col_no ] );
		if( value < mm.min ){
		    mm.min = value;
		}

		if( value > mm.max ){
		    mm.max = value;
		}
	    }
	    in.close();
	}

	return mm;

    }

}
