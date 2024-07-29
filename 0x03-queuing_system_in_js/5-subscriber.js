#!/usr/bin/node
/**
 * Connect to redis server via redis client
 */
import { createClient } from 'redis';

const client = createClient();

client.on('error', (resError) => {
  console.log('Redis client not connected to the server:', resError.toString());
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const listener = (message) => console.log(message);

client.SUBSCRIBE('holberton school channel');

client.on('message', (channel, message) => {
  if (channel === 'holberton school channel') {
    if (message === 'KILL_SERVER') {
      client.UNSUBSCRIBE();
      client.QUIT();
    }
    listener(message);
  }
});
