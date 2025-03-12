import { Container, Card } from 'react-bootstrap';
import { IoPersonSharp } from 'react-icons/io5';
import { FaHouse } from 'react-icons/fa6';
import { FaBookOpen } from 'react-icons/fa';

function Home() {
  return (
    <div className='py-6 flex flex-col justify-center sm:py-12 space-y-6'>
      <div className='flex space-x-6 justify-center'>
        <Container className='p-6 max-w-lg bg-white rounded-xl shadow-md flex justify-center space-x-4 m-auto p-2'>
          <Card className='text-center p-4'>
            <Card.Img
              src='/ChronoSync.png'
              alt='Logo'
              className='img-fluid object-cover'
            />
          </Card>
        </Container>
        <Container className='p-6 max-w-lg bg-white rounded-xl shadow-md flex justify-center space-x-4 m-auto p-2'>
          <Card className='text-center p-8 bg-white text-black rounded-xl'>
            <p className=' font-bold text-white bg-black mb-4 p-2'>
              -ChronoSync-
              <br />
              Schedule Management System
            </p>
            <p className='text-md'>
              ChronoSync is a powerful tool designed to streamline the process
              of scheduling classes for a semester while optimizing seat
              allocation, instructor availability, and room assignments. Built
              with automation at its core, the system ensures that students can
              enroll in their required courses without conflicts and that
              administrators can manage scheduling constraints.
            </p>
          </Card>
        </Container>
      </div>

      <br />
      <div className='flex space-x-6'>
        <Container className='p-6 max-w-lg bg-white rounded-xl shadow-md flex justify-center space-x-4'>
          <Card className='p-3 text-center'>
            <div className='flex items-center justify-center mb-4'>
              <a href='/courses' className='text-black'>
                <FaBookOpen className='text-8xl' />
              </a>
            </div>
            Add Available Courses
          </Card>
        </Container>
        <Container className='p-6 max-w-lg bg-white rounded-xl shadow-md flex justify-center space-x-4'>
          <Card className='p-3 text-center'>
            <div className='flex items-center justify-center mb-4'>
              <a href='/Professors' className='text-black'>
                <IoPersonSharp className='text-8xl' />
              </a>
            </div>
            Manage Professors
          </Card>
        </Container>
        <Container className='p-6 max-w-lg bg-white rounded-xl shadow-md flex justify-center space-x-4'>
          <Card className='p-3 text-center'>
            <div className='flex items-center justify-center mb-4'>
              <a href='/rooms' className='text-black'>
                <FaHouse className='text-8xl' />
              </a>
            </div>
            Set Up Room Availability
          </Card>
        </Container>
      </div>
    </div>
  );
}

export default Home;
