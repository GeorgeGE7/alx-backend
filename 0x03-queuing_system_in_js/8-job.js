#!/usr/bin/node
/**
 * Writing the job creation function
 */
function createPushNotificationsJobs(jobs, queue) {
  if (!(jobs instanceof Array)) {
    throw new Error('Jobs is not an array');
  }
  for (let job of jobs) {
    job = queue.create('push_notification_code_3', job);
    job
      .on('complete', (result) => { /* eslint-disable-line no-unused-vars */
        console.log(`Notification job ${job.id} completed`);
      })
      .on('failed', (resError) => { /* eslint-disable-line no-unused-vars */
        console.log(`Notification job ${job.id} failed: ${resError.message || resError.toString()}`);
      })
      .on('progress', (progress, data) => { /* eslint-disable-line no-unused-vars */
        console.log(`Notification job ${job.id} ${progress}% complete`);
      })
      .save((resError) => { /* eslint-disable-line no-unused-vars */
        console.log(`Notification job created: ${job.id}`);
      });
  }
}

module.exports = createPushNotificationsJobs;
