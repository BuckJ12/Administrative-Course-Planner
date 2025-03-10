import { Button, Card } from 'react-bootstrap';

function InvalidRoute() {
  return (
    <div style={{ textAlign: 'center' }}>
      <br />
      <Card className='text-center p-4'>
        <a href='/home' className='text-black'>
          <Card.Img
            src='/ChronoSync.png'
            alt='Logo'
            className='img-fluid object-cover'
          />
        </a>
      </Card>
      <br />
      <br />
      <h1>404 - Not Found</h1>
      <p>The page you are looking for does not exist.</p>
      <Button href='/home'>Go Home</Button>
    </div>
  );
}

export default InvalidRoute;
