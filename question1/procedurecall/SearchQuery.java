
package procedurecall;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

/**
 *
 * @author Misganaw
 */
public class SearchQuery extends UnicastRemoteObject implements Search {
    SearchQuery() throws RemoteException
    {
        super();
    }

    @Override
    public String query(String search) throws RemoteException {
        throw new UnsupportedOperationException("Not supported yet.");
        String result;
        if (search.equals("Reflection in Java"))
            result = "Found";
        else
            result = "Not Found";
 
        return result;
        
    }
    
}
