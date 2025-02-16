import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [newName, setNewName] = useState('');
  const [newRole, setNewRole] = useState('');

    useEffect(() => {
        const fetchAgents = async () => {
            try {
                const response = await axios.get('http://localhost:8000/agents');
                setAgents(response.data);
            } catch (error) {
                console.error("Error fetching agents:", error);
            }
        };

        fetchAgents();
      }, []);
    
        const handleCreateAgent = async (event) => {
            event.preventDefault();
            try {
                const response = await axios.post('http://localhost:8000/agents', {
                    name: newName,
                    role: newRole
                });
                setAgents([...agents, response.data]);
                setNewName('');
                setNewRole('');
            } catch (error) {
                console.error("Error creating agent:", error);
            }
        };
    
        const handleUpdateAgent = async (event) => {
            event.preventDefault();
            if (!selectedAgent) return;
            try {
                const response = await axios.put(`http://localhost:8000/agents/${selectedAgent.id}`, {
                    name: newName,
                    role: newRole
                });
                setAgents(agents.map(agent => (agent.id === selectedAgent.id ? response.data : agent)));
                setSelectedAgent(null);
                setNewName('');
                setNewRole('');
            } catch (error) {
                console.error("Error updating agent:", error);
            }
        };
        
        const handleDeleteAgent = async (agentId) => {
          try {
            await axios.delete(`http://localhost:8000/agents/${agentId}`);
            setAgents(agents.filter(agent => agent.id !== agentId));
            setSelectedAgent(null);
          } catch (error) {
            console.error("Error deleting agent:", error);
          }
        };

    const handleSelectAgent = (agent) => {
        setSelectedAgent(agent);
        setNewName(agent.name);
        setNewRole(agent.role);
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Trading Bot Dashboard</h1>
                <h2>Agents</h2>
                <ul>
                    {agents.map(agent => (
                        <li key={agent.id} onClick={() => handleSelectAgent(agent)}>
                            {agent.name} ({agent.role})
                            <button onClick={(e) => { e.stopPropagation(); handleDeleteAgent(agent.id); }}>Delete</button>
                        </li>
                      ))}
                    </ul>

                <h3>Create Agent</h3>
                <form onSubmit={handleCreateAgent}>
                    <input
                        type="text"
                        placeholder="Name"
                        value={newName}
                        onChange={(e) => setNewName(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Role"
                        value={newRole}
                        onChange={(e) => setNewRole(e.target.value)}
                    />
                    <button type="submit">Create</button>
                </form>

                {selectedAgent && (
                    <>
                        <h3>Update Agent</h3>
                        <form onSubmit={handleUpdateAgent}>
                            <input
                                type="text"
                                placeholder="Name"
                                value={newName}
                                onChange={(e) => setNewName(e.target.value)}
                            />
                            <input
                                type="text"
                                placeholder="Role"
                                value={newRole}
                                onChange={(e) => setNewRole(e.target.value)}
                            />
                            <button type="submit">Update</button>
                        </form>
                    </>
                )}
            </header>
        </div>
    );
}

export default App;