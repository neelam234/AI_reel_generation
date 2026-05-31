import { useState, useEffect } from 'react'
import { Plus, Video, Image as ImageIcon, Play, CheckCircle, Loader2, AlertCircle } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import { projectApi } from './api/projectApi'
import type { Project } from './types'
import './App.css'

function App() {
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Poll for status updates if processing
  useEffect(() => {
    let interval: number;
    if (project?.status === 'processing') {
      interval = setInterval(async () => {
        try {
          const updatedProject = await projectApi.getProject(project.id);
          setProject(updatedProject);
          if (updatedProject.status === 'completed' || updatedProject.status === 'failed') {
            clearInterval(interval);
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [project?.status, project?.id]);

  const createNewProject = async () => {
    setLoading(true);
    try {
      const newProject = await projectApi.createProject({ title: `New Reel ${new Date().toLocaleTimeString()}` });
      setProject(newProject);
      setError(null);
    } catch (err) {
      setError("Failed to create project");
    } finally {
      setLoading(false);
    }
  };

  const onDropVideo = async (acceptedFiles: File[]) => {
    if (!project || acceptedFiles.length === 0) return;
    setLoading(true);
    try {
      await projectApi.uploadReference(project.id, acceptedFiles[0]);
      const updated = await projectApi.getProject(project.id);
      setProject(updated);
    } catch (err) {
      setError("Video upload failed");
    } finally {
      setLoading(false);
    }
  };

  const onDropImages = async (acceptedFiles: File[]) => {
    if (!project || acceptedFiles.length === 0) return;
    setLoading(true);
    try {
      await projectApi.uploadImages(project.id, acceptedFiles);
      const updated = await projectApi.getProject(project.id);
      setProject(updated);
    } catch (err) {
      setError("Images upload failed");
    } finally {
      setLoading(false);
    }
  };

  const startGeneration = async () => {
    if (!project) return;
    setLoading(true);
    try {
      await projectApi.generateReel(project.id);
      setProject({ ...project, status: 'processing' });
    } catch (err) {
      setError("Failed to start generation");
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps: getVideoProps, getInputProps: getVideoInput } = useDropzone({
    onDrop: onDropVideo,
    accept: { 'video/*': ['.mp4', '.mov'] },
    multiple: false
  });

  const { getRootProps: getImagesProps, getInputProps: getImagesInput } = useDropzone({
    onDrop: onDropImages,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png'] }
  });

  return (
    <div className="app-container">
      <header className="header">
        <h1>AI Reel Gen</h1>
        {!project && (
          <button className="btn btn-primary" onClick={createNewProject} disabled={loading}>
            <Plus size={18} style={{ marginRight: '8px' }} />
            New Project
          </button>
        )}
      </header>

      {error && (
        <div className="card" style={{ borderColor: 'var(--error)', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <AlertCircle color="var(--error)" />
          <span>{error}</span>
        </div>
      )}

      {project && (
        <div className="project-view">
          <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h2 style={{ margin: 0 }}>{project.title}</h2>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: '4px 0 0 0' }}>ID: {project.id}</p>
            </div>
            <span className={`status-badge status-${project.status}`}>
              {project.status}
            </span>
          </div>

          <div className="upload-grid">
            <div className="card">
              <h3>1. Reference Video</h3>
              {project.reference_video ? (
                <div style={{ textAlign: 'center' }}>
                  <CheckCircle color="var(--success)" size={48} />
                  <p>Video Uploaded</p>
                  <button className="btn" onClick={() => setProject({...project, reference_video: undefined})}>Replace</button>
                </div>
              ) : (
                <div {...getVideoProps()} className="dropzone">
                  <input {...getVideoInput()} />
                  <Video size={32} color="var(--primary)" />
                  <p>Drop your reference video here</p>
                </div>
              )}
            </div>

            <div className="card">
              <h3>2. Product Images</h3>
              <div {...getImagesProps()} className="dropzone">
                <input {...getImagesInput()} />
                <ImageIcon size={32} color="var(--primary)" />
                <p>Add product images</p>
              </div>
              <div className="image-strip">
                {project.product_images.map((img, i) => (
                  <img key={i} src={`http://localhost:8001/${img}`} className="image-preview" alt="" />
                ))}
              </div>
            </div>
          </div>

          <div style={{ textAlign: 'center' }}>
            {project.status === 'created' && (
              <button 
                className="btn btn-primary" 
                style={{ padding: '1rem 3rem', fontSize: '1.1rem' }}
                disabled={!project.reference_video || project.product_images.length === 0 || loading}
                onClick={startGeneration}
              >
                {loading ? <Loader2 className="animate-spin" /> : <Play size={20} style={{ marginRight: '8px' }} />}
                Generate Reel
              </button>
            )}

            {project.status === 'processing' && (
              <div className="card">
                <Loader2 className="animate-spin" size={48} color="var(--primary)" />
                <h2>Rendering your reel...</h2>
                <p>This usually takes 30-60 seconds.</p>
              </div>
            )}

            {project.status === 'completed' && project.output_video && (
              <div className="card">
                <h2>✨ Reel Ready!</h2>
                <video 
                  className="video-preview" 
                  controls 
                  src={`http://localhost:8001/${project.output_video}`}
                />
                <div style={{ marginTop: '1rem' }}>
                  <button className="btn btn-primary" onClick={() => window.open(`http://localhost:8001/${project.output_video}`)}>
                    Download Reel
                  </button>
                  <button className="btn" style={{ marginLeft: '1rem' }} onClick={() => setProject(null)}>
                    Create Another
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {!project && !loading && (
        <div style={{ textAlign: 'center', marginTop: '10vh', color: 'var(--text-muted)' }}>
          <Video size={64} style={{ marginBottom: '1rem', opacity: 0.5 }} />
          <h2>No active project</h2>
          <p>Create a new project to start generating fashion reels.</p>
        </div>
      )}
    </div>
  )
}

export default App
