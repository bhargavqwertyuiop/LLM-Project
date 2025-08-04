import React, { useState, useCallback } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  FormControlLabel,
  Checkbox,
  FormGroup,
  CircularProgress,
  Alert,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
} from '@mui/material';
import {
  CloudUpload,
  Analytics,
  ExpandMore,
  Psychology,
  Mood,
  Topic,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

interface AnalysisResult {
  summary?: any;
  sentiment?: any;
  topics?: any;
  embeddings?: any;
}

interface DocumentInfo {
  filename: string;
  file_type: string;
  word_count: number;
  char_count: number;
}

const AnalysisPage: React.FC = () => {
  const [textInput, setTextInput] = useState('');
  const [analysisTypes, setAnalysisTypes] = useState({
    summary: true,
    sentiment: true,
    topics: true,
    embeddings: false,
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [documentInfo, setDocumentInfo] = useState<DocumentInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setResults(null);
    setDocumentInfo(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const analysisTypesString = Object.entries(analysisTypes)
        .filter(([_, enabled]) => enabled)
        .map(([type, _]) => type)
        .join(',');
      
      formData.append('analysis_types', analysisTypesString);

      const response = await axios.post('/api/v1/analyze-document', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data.analysis);
      setDocumentInfo(response.data.document_info);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze document');
    } finally {
      setLoading(false);
    }
  }, [analysisTypes]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
    },
    multiple: false,
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  const handleTextAnalysis = async () => {
    if (!textInput.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);
    setDocumentInfo(null);

    try {
      const analysisTypesArray = Object.entries(analysisTypes)
        .filter(([_, enabled]) => enabled)
        .map(([type, _]) => type);

      const response = await axios.post('/api/v1/analyze', {
        text: textInput,
        analysis_types: analysisTypesArray,
      });

      setResults(response.data.analysis_results);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze text');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalysisTypeChange = (type: string) => {
    setAnalysisTypes(prev => ({
      ...prev,
      [type]: !prev[type as keyof typeof prev],
    }));
  };

  const renderSummaryResults = (summary: any) => {
    if (!summary) return null;

    return (
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Psychology sx={{ mr: 1, color: 'primary.main' }} />
            <Typography variant="h6">Text Summarization</Typography>
          </Box>
          
          {summary.ollama && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Ollama ({summary.ollama.model})
              </Typography>
              <Paper sx={{ p: 2, backgroundColor: 'grey.50' }}>
                <ReactMarkdown>{summary.ollama.summary}</ReactMarkdown>
              </Paper>
            </Box>
          )}
          
          {summary.huggingface && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Hugging Face ({summary.huggingface.model})
              </Typography>
              <Paper sx={{ p: 2, backgroundColor: 'grey.50' }}>
                <Typography>{summary.huggingface.summary}</Typography>
              </Paper>
            </Box>
          )}
        </CardContent>
      </Card>
    );
  };

  const renderSentimentResults = (sentiment: any) => {
    if (!sentiment || sentiment.error) return null;

    const getSentimentColor = (label: string) => {
      switch (label.toLowerCase()) {
        case 'positive':
        case 'label_2':
          return 'success';
        case 'negative':
        case 'label_0':
          return 'error';
        default:
          return 'warning';
      }
    };

    return (
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Mood sx={{ mr: 1, color: 'secondary.main' }} />
            <Typography variant="h6">Sentiment Analysis</Typography>
          </Box>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
            <Chip
              label={sentiment.overall_sentiment}
              color={getSentimentColor(sentiment.overall_sentiment)}
              variant="filled"
            />
            <Typography variant="body2">
              Confidence: {(sentiment.confidence * 100).toFixed(1)}%
            </Typography>
          </Box>
          
          {sentiment.detailed_results && (
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="subtitle2">Detailed Results</Typography>
              </AccordionSummary>
              <AccordionDetails>
                {sentiment.detailed_results.map((result: any, index: number) => (
                  <Box key={index} sx={{ mb: 1 }}>
                    <Chip
                      label={`${result.label}: ${(result.score * 100).toFixed(1)}%`}
                      color={getSentimentColor(result.label)}
                      variant="outlined"
                      size="small"
                    />
                  </Box>
                ))}
              </AccordionDetails>
            </Accordion>
          )}
        </CardContent>
      </Card>
    );
  };

  const renderTopicsResults = (topics: any) => {
    if (!topics || topics.error) return null;

    return (
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Topic sx={{ mr: 1, color: 'info.main' }} />
            <Typography variant="h6">Key Topics</Typography>
          </Box>
          
          <Paper sx={{ p: 2, backgroundColor: 'grey.50' }}>
            <ReactMarkdown>{topics.topics}</ReactMarkdown>
          </Paper>
        </CardContent>
      </Card>
    );
  };

  return (
    <Container maxWidth="xl">
      <Typography variant="h2" component="h1" gutterBottom textAlign="center">
        Document Analysis
      </Typography>
      <Typography variant="h6" color="text.secondary" textAlign="center" sx={{ mb: 4 }}>
        Upload documents or enter text for AI-powered analysis
      </Typography>

      <Grid container spacing={4}>
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Input
            </Typography>

            {/* File Upload */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Upload Document
              </Typography>
              <Paper
                {...getRootProps()}
                sx={{
                  p: 4,
                  textAlign: 'center',
                  border: '2px dashed',
                  borderColor: isDragActive ? 'primary.main' : 'grey.300',
                  backgroundColor: isDragActive ? 'primary.50' : 'grey.50',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  '&:hover': {
                    borderColor: 'primary.main',
                    backgroundColor: 'primary.50',
                  },
                }}
              >
                <input {...getInputProps()} />
                <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  {isDragActive ? 'Drop the file here' : 'Drag & drop a file here'}
                </Typography>
                <Typography color="text.secondary">
                  or click to select a file
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Supports: PDF, DOCX, TXT, PPTX, XLSX, CSV (max 50MB)
                </Typography>
              </Paper>
            </Box>

            <Divider sx={{ my: 3 }}>OR</Divider>

            {/* Text Input */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Enter Text
              </Typography>
              <TextField
                fullWidth
                multiline
                rows={8}
                placeholder="Enter your text here for analysis..."
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                variant="outlined"
              />
            </Box>

            {/* Analysis Options */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Analysis Types
              </Typography>
              <FormGroup row>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={analysisTypes.summary}
                      onChange={() => handleAnalysisTypeChange('summary')}
                    />
                  }
                  label="Summarization"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={analysisTypes.sentiment}
                      onChange={() => handleAnalysisTypeChange('sentiment')}
                    />
                  }
                  label="Sentiment Analysis"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={analysisTypes.topics}
                      onChange={() => handleAnalysisTypeChange('topics')}
                    />
                  }
                  label="Topic Extraction"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={analysisTypes.embeddings}
                      onChange={() => handleAnalysisTypeChange('embeddings')}
                    />
                  }
                  label="Generate Embeddings"
                />
              </FormGroup>
            </Box>

            {/* Analyze Button */}
            <Button
              variant="contained"
              size="large"
              startIcon={loading ? <CircularProgress size={20} /> : <Analytics />}
              onClick={handleTextAnalysis}
              disabled={loading || !textInput.trim()}
              fullWidth
            >
              {loading ? 'Analyzing...' : 'Analyze Text'}
            </Button>
          </Paper>
        </Grid>

        {/* Results Section */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, minHeight: 400 }}>
            <Typography variant="h5" gutterBottom>
              Results
            </Typography>

            {loading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                <CircularProgress />
              </Box>
            )}

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            {documentInfo && (
              <Card sx={{ mb: 2, backgroundColor: 'info.50', borderColor: 'info.main' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Document Information
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Filename:</strong> {documentInfo.filename}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Type:</strong> {documentInfo.file_type}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Word Count:</strong> {documentInfo.word_count.toLocaleString()}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Character Count:</strong> {documentInfo.char_count.toLocaleString()}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            )}

            {results && (
              <Box>
                {renderSummaryResults(results.summary)}
                {renderSentimentResults(results.sentiment)}
                {renderTopicsResults(results.topics)}
                
                {results.embeddings && (
                  <Card sx={{ mb: 2 }}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Embeddings Generated
                      </Typography>
                      <Typography color="text.secondary">
                        Vector length: {results.embeddings.vector_length}
                      </Typography>
                    </CardContent>
                  </Card>
                )}
              </Box>
            )}

            {!loading && !results && !error && (
              <Box sx={{ textAlign: 'center', py: 4, color: 'text.secondary' }}>
                <Analytics sx={{ fontSize: 64, mb: 2 }} />
                <Typography variant="h6">
                  Upload a document or enter text to see analysis results
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default AnalysisPage;