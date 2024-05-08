// pages/index.js
import { useState } from 'react';

export default function Home() {
  const [formData, setFormData] = useState({
    age: '',
    address: '',
    symptoms: '',
  });
  const [diagnosis, setDiagnosis] = useState('');
  const [severity, setSeverity] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // This is where we'd trigger the function to send data to the LLM
    // For now, we'll just log the form data
    console.log(formData);
    // You'd replace the below lines with your actual API call
    const mockDiagnosis = 'Sample Diagnosis';
    const mockSeverity = 'Stage 1';
    setDiagnosis(mockDiagnosis);
    setSeverity(mockSeverity);
  };

  return (
    <div>
      <h1>AI Health Assistant</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="age"
          value={formData.age}
          onChange={handleChange}
          placeholder="Age"
          required
        />
        <input
          type="text"
          name="address"
          value={formData.address}
          onChange={handleChange}
          placeholder="Address"
          required
        />
        <textarea
          name="symptoms"
          value={formData.symptoms}
          onChange={handleChange}
          placeholder="Describe your symptoms"
          required
        />
        <button type="submit">Send</button>
      </form>
      {diagnosis && <p>Diagnosis: {diagnosis}</p>}
      {severity && <p>Severity: {severity}</p>}
    </div>
  );
}
