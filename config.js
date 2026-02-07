// Submission window configuration
// Modify these values to control when submissions are accepted

module.exports = {
  // Submission window start time (ISO 8601 format)
  windowOpen: process.env.SUBMISSION_WINDOW_OPEN || '2026-02-07T00:00:00Z',

  // Submission window end time (ISO 8601 format)
  windowClose: process.env.SUBMISSION_WINDOW_CLOSE || '2026-02-14T23:59:59Z',

  // Server port
  port: process.env.PORT || 3000,

  // Path to store submissions
  dataDir: './data',
  submissionsFile: './data/submissions.json',
};
