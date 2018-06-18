import java.io.*;

public class EvaluateTable {

    public static void main( String[] args ) throws Exception{

	//args:
	//0: table
	//1-N: data files

	final Table t = new Table( args[ 0 ] );

	for( int i=1; i<args.length; ++i ){
	    final String filename = args[ i ];
	    final BufferedReader in = new BufferedReader( new FileReader( filename ) );
	    for( String line = in.readLine(); line != null; line = in.readLine() ){
		evaluateLine( t, line );
	    }
	    in.close();

	}
    }

    public void evaluateLine( final Table t, final String line ){
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


	final
    }

}
