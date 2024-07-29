#!/usr/bin/node
/**
 * Connect to redis server via redis client
 */
import { promisify } from 'util';
import { createClient, print } from 'redis';

const client = createClient();

client.on('error', (resError) => {
  console.log('Redis client not connected to the server:', resError.toString());
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

function setNewSchool(schoolName, value) {
  client.SET(schoolName, value, print);
}

async function displaySchoolValue(schoolName) {
  const GET = promisify(client.GET).bind(client);
  try {
    const value = await GET(schoolName);
    console.log(value);
  } catch (error) {
    console.log(error.toString());
  }
}

(async () => {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
})();
