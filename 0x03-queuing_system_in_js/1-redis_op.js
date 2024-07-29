#!/usr/bin/node
/**
 * Connect to redis server via redis client
 */
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

function displaySchoolValue(schoolName) {
  client.GET(schoolName, (resError, value) => {
    console.log(value);
  });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
