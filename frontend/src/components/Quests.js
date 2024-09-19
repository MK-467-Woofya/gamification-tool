import axios from "axios";
import {useState, useEffect } from "react";

/**
 * Quests view where users are given tasks to complete in exchange for points
 * 
 */
export const Quests = () => {

  const [user, setUser] = useState(null);
  // get user from Gamification API
  useEffect(() => {
      console.log('Fetching user data...'); // useEffect

      const url = "http://localhost:8000/api/users/username/";
      const username = sessionStorage.getItem('username');

      const headers = {
          'Content-Type': 'application/json',
          'Gamification-Api-Key': process.env.REACT_APP_API_KEY
      };
      
      axios.get(url + username + '/', { headers })

          .then(response => {
              console.log('User data fetched:', response.data); // data grab
              setUser(response.data);
          })
          .catch(error => {
              console.error('Error fetching user data:', error);
          });
  }, []);

  // state values to update
  const [experience_points, setExperiencePoints] = useState(null);
  const [shop_points, setShopPoints] = useState(null);

  const handleChange = (evt) => {
    const value = evt.target.value;

    setExperiencePoints(value);
    setShopPoints(value);
  };

  const submitForm = (e) => {
    e.preventDefault();
    console.log(e);
    console.log(experience_points);
    console.log(shop_points);

    const id = user.id
    const url = "http://localhost:8000/api/users/" + id + "/update_points/"

    const data = {
      'experience_points': experience_points,
      'shop_points': shop_points
    };
    // header including env variable of the API Key
    const headers = {
        'Content-Type': 'application/json',
        'Gamification-Api-Key': process.env.REACT_APP_API_KEY
    };
    // increase user points by submitted amount
    axios.patch(url, data, { headers })

        .then(res => {
            console.log('User points increased:', res.data); // data grab
            setUser(prevUser => ({...prevUser, data}))
            console.log('USER: ', user)
        })
        .catch(error => {
            console.error('Error patching user points:', error);
        });
  };
  // while user being accessed
  if (!user) { // return this while loading
    return <div>Loading...</div>;
  }

  // placeholder button to increase user experience & shop points
  return (
    <div className="form-signin mt-5 text-center">
      <p>Experience points: {user.experience_points}</p>
      <p>Shop points: {user.shop_points}<br/></p>
      <p>Add points:</p>
      <div>
        <form onSubmit={submitForm}>
          <label>
            Experience Points:
            <input
              type="number"
              name="experience_points"
              placeholder="100"
              value={experience_points}
              onChange={handleChange}
            />
            Shop Points:
            <input
              type="number"
              name="shop_points"
              placeholder="100"
              value={shop_points}
              onChange={handleChange}
            />
          </label>
          <button type="submit">Add</button>
        </form>
      </div>
    </div>
  );
}