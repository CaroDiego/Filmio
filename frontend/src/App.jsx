  import './App.css'
import FetchTest from './components/Test/FetchTest';
import UploadFile from './components/UploadFile/UploadFile';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <h1>Upload your .zip file</h1>
      </header>
      <main>
        <UploadFile />
        <FetchTest />
      </main>
    </div>
  );
}

export default App
