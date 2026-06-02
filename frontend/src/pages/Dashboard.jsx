// Main protected dashboard page.
import { useEffect, useState } from "react";
import { apiRequest } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";
import AnimalCard from "../components/AnimalCard.jsx";

const emptyAnimal = {
  name: "",
  species: "",
  breed: "",
  gender: "",
  date_of_birth: "",
};

function Dashboard() {
  const { user } = useAuth();
  const [animals, setAnimals] = useState([]);
  const [reminders, setReminders] = useState([]);
  const [form, setForm] = useState(emptyAnimal);
  const [error, setError] = useState("");

  // useEffect loads protected backend data after login.
  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      const [animalData, reminderData] = await Promise.all([
        apiRequest("/animals"),
        apiRequest("/reminders"),
      ]);
      setAnimals(animalData);
      setReminders(reminderData);
    } catch (err) {
      setError(err.message);
    }
  }

  function handleChange(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function addAnimal(event) {
    event.preventDefault();
    setError("");

    try {
      const newAnimal = await apiRequest("/animals", {
        method: "POST",
        body: JSON.stringify(form),
      });
      setAnimals([newAnimal, ...animals]);
      setForm(emptyAnimal);
    } catch (err) {
      setError(err.message);
    }
  }

  async function toggleFavorite(animal) {
    try {
      const method = animal.is_favorite ? "DELETE" : "POST";
      await apiRequest(`/animals/${animal.id}/favorite`, { method });
      loadDashboard();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Protected dashboard</p>
          <h1>Welcome, {user?.username}</h1>
        </div>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="grid two-columns">
        <form className="card form" onSubmit={addAnimal}>
          <h2>Add Animal</h2>
          <label>Name<input name="name" value={form.name} onChange={handleChange} required /></label>
          <label>Species<input name="species" value={form.species} onChange={handleChange} required placeholder="Cow, Goat, Sheep" /></label>
          <label>Breed<input name="breed" value={form.breed} onChange={handleChange} /></label>
          <label>Gender<input name="gender" value={form.gender} onChange={handleChange} /></label>
          <label>Date of Birth<input type="date" name="date_of_birth" value={form.date_of_birth} onChange={handleChange} /></label>
          <button type="submit">Save Animal</button>
        </form>

        <div className="card">
          <h2>Upcoming reminders</h2>
          {reminders.length === 0 ? (
            <p>No reminders due in the next 30 days.</p>
          ) : (
            <ul className="reminder-list">
              {reminders.map((reminder) => (
                <li key={reminder.id}>
                  <strong>{reminder.animal_name}</strong>: {reminder.title} due on {reminder.due_date}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <h2>Your animals</h2>
      <div className="animal-list">
        {animals.length === 0 ? (
          <p>No animals yet. Add your first animal above.</p>
        ) : (
          animals.map((animal) => (
            <AnimalCard key={animal.id} animal={animal} onToggleFavorite={toggleFavorite} />
          ))
        )}
      </div>
    </section>
  );
}

export default Dashboard;
