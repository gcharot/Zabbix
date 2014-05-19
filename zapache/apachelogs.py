"""apachelogs.py: code for reading and parsing Apache log files.

Sample use -- counting the number of 40xs seen:

  import apachelogs

  alf = ApacheLogFile('access.log')
  40x_count = 0
  for log_line in alf:
    if log_line.http_response_code.startswith('40'):
      40x_count += 1
  alf.close()
  print "Saw %d 40x responses" % 40x_count

Copyright (c) 2007, Kevin Scott 
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
     * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
     * Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
     * The name of the author may be used to endorse or promote products
       derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY <copyright holder> ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__ = 'Kevin Scott (kevin.scott@gmail.com)'

import re
import time

class ApacheLogLine:
  """A Python class whose attributes are the fields of Apache log line.

  Designed specifically with combined format access logs in mind.  For
  example, the log line

  127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08 [en] (Win98; I ;Nav)"

  would have the following field values as an ApacheLogLine:

  ip = '127.0.0.1'
  ident = '-'
  http_user = 'frank'
  time = '10/Oct/2000:13:55:36 -0700'
  request_line = 'GET /apache_pb.gif HTTP/1.0'
  http_response_code = '200'
  http_response_size = 2326
  referrer = 'http://www.example.com/start.html'
  user_agent = 'Mozilla/4.08 [en] (Win98; I ;Nav)'

  Typically you would only read from instances of ApacheLogLine.  Some other
  code, e.g., that in ApacheLogFile._ApacheLogFileGenerator, should be relied
  upon to parse the log lines and instantiate appropriate ApacheLogLine 
  instances.
  """

  def __init__(self, ip, id, hu, t, rl, hrc, hrs, r, ua): 
    self.ip = ip
    self.ident = id
    self.http_user = hu
    self.time = t
    self.request_line = rl
    self.http_response_code = hrc
    self.http_response_size = hrs
    self.referrer = r
    self.user_agent = ua

  def __str__(self):
    """Return a simple string representation of an ApacheLogLine."""
    return ','.join([self.ip, self.ident, self.time, self.request_line,
        self.http_response_code, self.http_response_size, self.referrer,
        self.user_agent])

class ApacheLogFile:
  """An abstraction for reading and parsing Apache log files."""

  class _ApacheLogFileGenerator:
    """Helper for iterating over log lines and instantiating ApacheLogLines."""
    def __init__(self, f):
      self.f = f
      # We only compile the regular expression which handles the log line
      # parsing once per pass over the file, i.e., when client code asks for
      # an iterator.
      self.r = re.compile(r'(\d+\.\d+\.\d+\.\d+) (.*) (.*) \[(.*)\] "(.*)" (\d+) (.*) "(.*)" "(.*)"')

    def Generator(self):
      """Generator which yields parsed ApacheLogLines from log file lines."""
      for line in self.f:
        m = self.r.match(line)
        if m:
          log_line = ApacheLogLine(m.group(1), m.group(2), m.group(3),
              m.group(4), m.group(5), m.group(6), m.group(7), m.group(8),
              m.group(9))
          yield log_line

  def __init__(self, filename):
    """Instantiating an ApacheLogFile opens a log file.  
    
    Client is responsible for closing the opened log file by calling close()"""
    self.f = open(filename)

  def close(self):
    """Closes the actual Apache log file."""
    self.f.close()

  def __iter__(self):
    """Builds an iterator from gen.Generator."""
    gen = ApacheLogFile._ApacheLogFileGenerator(self.f)
    return gen.Generator()
