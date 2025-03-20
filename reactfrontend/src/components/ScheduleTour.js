import React, { useState } from 'react';
import { scheduleTour } from '../services/api';

const ScheduleTour = () => {
  const [tourId, setTourId] = useState('');
  const [startTime, setStartTime] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!tourId || !startTime) {
      setErrorMessage('Tour ID and Start Time cannot be empty');
      return;
    }

    try {
      const formattedStartTime = startTime.replace('T', ' ');
      const response = await scheduleTour(tourId, formattedStartTime);
      setSuccessMessage(response.message);
      setErrorMessage('');
    } catch (error) {
      setErrorMessage(error.error || 'Scheduling failed, please try again');
      setSuccessMessage('');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto', fontFamily: 'Arial, sans-serif' }}>
      <h2 style={{ textAlign: 'center' }}>Schedule Tour</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <div>
          <label htmlFor="tourId" style={{ display: 'block', fontWeight: 'bold' }}>Tour ID:</label>
          <input
            type="text"
            id="tourId"
            name="tourId"
            value={tourId}
            onChange={(e) => setTourId(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', fontSize: '14px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>

        <div>
          <label htmlFor="startTime" style={{ display: 'block', fontWeight: 'bold' }}>Start Time:</label>
          <input
            type="datetime-local"
            id="startTime"
            name="startTime"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', fontSize: '14px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>

        <button
          type="submit"
          style={{
            padding: '10px 20px',
            backgroundColor: 'skyblue',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Submit
        </button>

        {successMessage && <p style={{ color: 'green', textAlign: 'center' }}>{successMessage}</p>}
        {errorMessage && <p style={{ color: 'red', textAlign: 'center' }}>{errorMessage}</p>}
      </form>
    </div>
  );
};

export default ScheduleTour;
