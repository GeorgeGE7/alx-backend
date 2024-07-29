#!/usr/bin/node
/**
 * Can I have a seat
 */
import { promisify } from 'util';
import { createClient } from 'redis';
import { createQueue } from 'kue';
import express from 'express';

let reservationEnabled;
const redisClient = createClient();

redisClient.on('error', (resError) => {
  console.log('Redis client not connected to the server:', resError.toString());
});

function reserveSeat(number) {
  return redisClient.SET('available_seats', number);
}

function getCurrentAvailableSeats() {
  const GET = promisify(redisClient.GET).bind(redisClient);
  return GET('available_seats');
}

const queue = createQueue();

const app = express();

app.get('/available_seats', (req, res) => {
  getCurrentAvailableSeats()
    .then((seats) => {
      res.json({ numberOfAvailableSeats: seats });
    })
    .catch((resError) => {
      console.log(resError);
      res.status(500).json(null);
    });
});

app.get('/reserve_seat', (req, res) => { /* eslint-disable-line consistent-return */
  if (reservationEnabled === false) {
    return res.json({ status: 'Reservation are blocked' });
  }
  const job = queue.create('reserve_seat', { task: 'reserve a seat' });
  job
    .on('complete', (status) => { /* eslint-disable-line no-unused-vars */
      console.log(`Seat reservation job ${job.id} completed`);
    })
    .on('failed', (resError) => {
      console.log(`Seat reservation job ${job.id} failed: ${resError.message || resError.toString()}`);
    })
    .save((resError) => {
      if (resError) return res.json({ status: 'Reservation failed' });
      return res.json({ status: 'Reservation in process' });
    });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    let availableSeats = await getCurrentAvailableSeats();
    availableSeats -= 1;
    reserveSeat(availableSeats);
    if (availableSeats >= 0) {
      if (availableSeats === 0) reservationEnabled = false;
      done();
    }
    done(new Error('Not enough seats available'));
  });
});

app.listen(1245, () => {
  reserveSeat(50);
  reservationEnabled = true;
  console.log('API available on localhost via port 1245');
});
