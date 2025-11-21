import { Link } from 'react-router-dom';

const Detail = () => {
  return (
    <div className="my_content">
      <h3>Welcome to</h3>
      <h1>AutoScope</h1>
      <p>Your one-stop solution for automated code analysis and insights.</p>
      <Link to="/dashboard">
        <button className="btn btn-primary">Get Started</button>
      </Link>
    </div>
  );
};

export default Detail;
