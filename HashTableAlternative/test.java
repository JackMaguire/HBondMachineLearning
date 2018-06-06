import java.io.*;
public class test{

    public static void main(String[] args){

	System.out.println( "test_table_io(): " + test_table_io( false ) );
	System.out.println( "test_binForValue(): " + test_binForValue( false ) );

    }

    public static boolean test_table_io( boolean verbose ){
	final String filename = "temp_file";

	try {

	    final MinMax[] value_ranges = { new MinMax(0,1), new MinMax(1,10), new MinMax(-2,2) };
	    final Table t1 = new Table( 10, value_ranges );

	    t1.register( 0.5, 1, -1, true );
	    t1.register( 0.5, 2, -1.5, false );
	    t1.register( 0.5, 3, -0.1, true );
	    t1.register( 0.5, 4, 2, false );
	    t1.register( 0.5, 5, 1.2, true );
	    t1.register( 0.2, 6, 5, false );
	    t1.register( 0.2, 7, 0, true );
	    t1.register( 0.7, 8, 0.9, false );
	    t1.register( 0.7, 9, 0.2, true );
	    t1.register( 0.7, 9, 0.2, true );
	    t1.register( 0.7, 9, 0.2, true );
	    t1.register( 0.7, 9, 0.2, true );
	    t1.register( 0.7, 9, 0.2, true );
	    t1.register( 0.7, 9, 0.2, false );
	    t1.register( 0.7, 9, 0.2, false );
	    t1.register( 0.7, 9, 0.2, false );

	    t1.save( filename );

	    final Table t2 = new Table( filename );

	    final File f = new File( filename );
	    f.delete();
	    return t1.assert_equality( t2 );

	} catch( Exception e ){
	    System.err.println( e.getMessage() );
	    e.printStackTrace();
	    final File f = new File( filename );
	    //f.delete();
	    return false;
	}
	//File f = new File( filename );
	//f.delete();
	//return true;
    }


    public static boolean test_binForValue( boolean verbose ){
	try {
	    final MinMax range = new MinMax( -200, 50 );

	    for( int bins = 1; bins < 10; bins += 3 ){
		ASSERT_EQUALS( Table.binForValue( -200, range, bins ), 0 );
		ASSERT_EQUALS( Table.binForValue(   50, range, bins ), bins - 1 );
	    }

	    for( int bins = 1; bins < 10; bins += 3 ){
		ASSERT_EQUALS( Table.binForValue( -199, range, bins ), 0 );
		ASSERT_EQUALS( Table.binForValue(   49, range, bins ), bins - 1 );
	    }

	    if( verbose ){
		final MinMax range2 = new MinMax( 0, 10 );
		for( double x = -0.5; x < 11.0; x += 0.5 ){
		    System.out.println( x + " " + Table.binForValue( x, range2, 3 ) );
		}
	    }

	} catch ( Exception e ) {
	    System.err.println( e.getMessage() );
	    e.printStackTrace();
	    return false;
	}
	return true;
    }






    private static void ASSERT( boolean in ) throws Exception{
	if( ! in ){
	    throw new Exception();
	}
    }

    private static void ASSERT_EQUALS( Object a, Object b ) throws Exception{
	if( a != b ){
	    throw new Exception( a + " != " + b );
	}
    }


}

