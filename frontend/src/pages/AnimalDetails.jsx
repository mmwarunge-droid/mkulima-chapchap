// Protected page for viewing and updating one animal.
import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { apiRequest } from "../services/api.js";

function AnimalDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [animal, setAnimal] = useState(null);
  const [error, setError] = useState("");
  const [animalForm, setAnimalForm] = useState({});
  const [weightForm, setWeightForm] = useState({ weight_kg: "", measured_on: "", notes: "" });
  const [healthForm, setHealthForm] = useState({
    record_type: "vaccination",
    title: "",
    due_date: "",
    completed_on: "",
    cost: "",
    notes: "",
  });

  useEffect(() => {
    loadAnimal();
  }, [id]);

  async function loadAnimal() {
    try {
      const data = await apiRequest(`/animals/${id}`);
      setAnimal(data);
      setAnimalForm({
        name: data.name || "",
        species: data.species || "",
        breed: data.breed || "",
        gender: data.gender || "",
        date_of_birth: data.date_of_birth || "",
        status: data.status || "active",
        sale_price: data.sale_price || 0,
      });
    } catch (err) {
      setError(err.message);
    }
  }

  function changeAnimal(event) {
    setAnimalForm({ ...animalForm, [event.target.name]: event.target.value });
  }

  function changeWeight(event) {
    setWeightForm({ ...weightForm, [event.target.name]: event.target.value });
  }

  function changeHealth(event) {
    setHealthForm({ ...healthForm, [event.target.name]: event.target.value });
  }

  async function updateAnimal(event) {
    event.preventDefault();
    setError("");
    try {
      await apiRequest(`/animals/${id}`, {
        method: "PUT",
        body: JSON.stringify(animalForm),
      });
      loadAnimal();
    } catch (err) {
      setError(err.message);
    }
  }

  async function deleteAnimal() {
    if (!confirm("Delete this animal and all its records?")) return;

    try {
      await apiRequest(`/animals/${id}`, { method: "DELETE" });
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  }

  async function addWeight(event) {
    event.preventDefault();
    setError("");
    try {
      await apiRequest(`/animals/${id}/weights`, {
        method: "POST",
        body: JSON.stringify(weightForm),
      });
      setWeightForm({ weight_kg: "", measured_on: "", notes: "" });
      loadAnimal();
    } catch (err) {
      setError(err.message);
    }
  }

  async function deleteWeight(recordId) {
    try {
      await apiRequest(`/weights/${recordId}`, { method: "DELETE" });
      loadAnimal();
    } catch (err) {
      setError(err.message);
    }
  }

  async function addHealthRecord(event) {
    event.preventDefault();
    setError("");
    try {
      await apiRequest(`/animals/${id}/health-records`, {
        method: "POST",
        body: JSON.stringify(healthForm),
      });
      setHealthForm({ record_type: "vaccination", title: "", due_date: "", completed_on: "", cost: "", notes: "" });
      loadAnimal();
    } catch (err) {
      setError(err.message);
    }
  }

  async function markComplete(record) {
    const today = new Date().toISOString().slice(0, 10);
    try {
      await apiRequest(`/health-records/${record.id}`, {
        method: "PUT",
        body: JSON.stringify({ completed_on: today }),
      });
      loadAnimal();
    } catch (err) {
      setError(err.message);
    }
  }

  async function deleteHealthRecord(recordId) {
    try {
      await apiRequest(`/health-records/${recordId}`, { method: "DELETE" });
      loadAnimal();
    } catch (err) {
      setError(err.message);
    }
  }

  if (!animal) {
    return <p>{error || "Loading animal..."}</p>;
  }

  return (
    <section>
      <Link to="/dashboard">← Back to dashboard</Link>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Animal details</p>
          <h1>{animal.name}</h1>
        </div>
        <button className="danger" onClick={deleteAnimal}>Delete Animal</button>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="grid two-columns">
        <form className="card form" onSubmit={updateAnimal}>
          <h2>Edit Animal</h2>
          <label>Name<input name="name" value={animalForm.name} onChange={changeAnimal} required /></label>
          <label>Species<input name="species" value={animalForm.species} onChange={changeAnimal} required /></label>
          <label>Breed<input name="breed" value={animalForm.breed} onChange={changeAnimal} /></label>
          <label>Gender<input name="gender" value={animalForm.gender} onChange={changeAnimal} /></label>
          <label>Date of Birth<input type="date" name="date_of_birth" value={animalForm.date_of_birth} onChange={changeAnimal} /></label>
          <label>Status
            <select name="status" value={animalForm.status} onChange={changeAnimal}>
              <option value="active">Active</option>
              <option value="sold">Sold</option>
            </select>
          </label>
          <label>Sale Price<input type="number" name="sale_price" value={animalForm.sale_price} onChange={changeAnimal} /></label>
          <button type="submit">Update Animal</button>
        </form>

        <form className="card form" onSubmit={addWeight}>
          <h2>Add Weight</h2>
          <label>Weight KG<input type="number" step="0.1" name="weight_kg" value={weightForm.weight_kg} onChange={changeWeight} required /></label>
          <label>Measured On<input type="date" name="measured_on" value={weightForm.measured_on} onChange={changeWeight} /></label>
          <label>Notes<textarea name="notes" value={weightForm.notes} onChange={changeWeight} /></label>
          <button type="submit">Save Weight</button>
        </form>
      </div>

      <div className="grid two-columns">
        <form className="card form" onSubmit={addHealthRecord}>
          <h2>Add Health / Cost Record</h2>
          <label>Type
            <select name="record_type" value={healthForm.record_type} onChange={changeHealth}>
              <option value="vaccination">Vaccination</option>
              <option value="deworming">Deworming</option>
              <option value="medical">Medical</option>
              <option value="breeding">Breeding Cost</option>
            </select>
          </label>
          <label>Title<input name="title" value={healthForm.title} onChange={changeHealth} required /></label>
          <label>Due Date<input type="date" name="due_date" value={healthForm.due_date} onChange={changeHealth} /></label>
          <label>Completed On<input type="date" name="completed_on" value={healthForm.completed_on} onChange={changeHealth} /></label>
          <label>Cost<input type="number" name="cost" value={healthForm.cost} onChange={changeHealth} /></label>
          <label>Notes<textarea name="notes" value={healthForm.notes} onChange={changeHealth} /></label>
          <button type="submit">Save Record</button>
        </form>

        <div className="card">
          <h2>Weight History</h2>
          {animal.weights.length === 0 ? <p>No weights yet.</p> : (
            <ul className="record-list">
              {animal.weights.map((weight) => (
                <li key={weight.id}>
                  <span>{weight.measured_on}: {weight.weight_kg} KG</span>
                  <button className="small danger" onClick={() => deleteWeight(weight.id)}>Delete</button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="card">
        <h2>Health Records</h2>
        {animal.health_records.length === 0 ? <p>No health records yet.</p> : (
          <ul className="record-list">
            {animal.health_records.map((record) => (
              <li key={record.id}>
                <span>
                  <strong>{record.title}</strong> ({record.record_type}) — Due: {record.due_date || "N/A"} — Cost: KES {record.cost || 0}
                  {record.completed_on ? ` — Completed: ${record.completed_on}` : ""}
                </span>
                <div>
                  {!record.completed_on && <button className="small" onClick={() => markComplete(record)}>Mark Complete</button>}
                  <button className="small danger" onClick={() => deleteHealthRecord(record.id)}>Delete</button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}

export default AnimalDetails;
