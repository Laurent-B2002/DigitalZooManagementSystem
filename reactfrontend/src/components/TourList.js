import React, { useEffect, useState } from "react";
import { getTours } from "../services/api";

const TourList = () => {
  const [tours, setTours] = useState([]);

  useEffect(() => {
    fetchTours();
  }, []);

  const fetchTours = async () => {
    try {
      const toursData = await getTours();
      const toursWithRoutes = toursData.map(tour => ({
        ...tour,
        route: tour.route_details.map(route => route.habitat_name)
      }));
  
      setTours(toursWithRoutes);
    } catch (error) {
      console.error("Failed to fetch Tours:", error);
    }
  };

  return (
    <div>
      <h2>Tour List</h2>
      <ul>
        {tours.length === 0 ? <p>No tours available.</p> : null}
        {tours.map((tour, index) => (
          <li key={index}>
            No.{tour.id} - <strong>{tour.name}</strong>
            <br />
            <small>| Description: {tour.description}</small>
            <br />
            <small>| Duration: {tour.duration}</small>
            <br />
            <small>| Available Spots: {tour.available_spots}</small>
            <br />
            <small>| Scheduled: {tour.is_scheduled ? "Yes" : "No"}</small>
            <br />
            <small>| Start Time: {tour.start_time ? new Date(tour.start_time).toLocaleString() : "Not Scheduled"}</small>
            <br />
            <small>| Route: {tour.route.length > 0 ? tour.route.join(" → ") : "No Route Assigned"}</small>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TourList;