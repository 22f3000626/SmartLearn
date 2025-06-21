<%@ page import="java.sql.*" %>
<%
    String username = request.getParameter("name");
    String password = request.getParameter("password");

    try {
        Class.forName("com.mysql.cj.jdbc.Driver");
        Connection con = DriverManager.getConnection(
            "jdbc:mysql://localhost:3306/test_db?serverTimezone=UTC",
            "root",
            ""
        );
        PreparedStatement ps = con.prepareStatement(
            "SELECT * FROM USERS WHERE NAME=? AND Password=?"
        );
        ps.setString(1, username);
        ps.setString(2, password);
        
        ResultSet rs = ps.executeQuery();
        
        if(rs.next()) {
            out.println("<script>alert('Valid credentials!')</script>");
        } else {
            out.println("<script>alert('Invalid credentials!')</script>");
        }
        rs,close();
        con.close();
    } catch(Exception e) {
        out.println("<script>alert('Error: " + e.getMessage() + "')</script>");
    }
%>