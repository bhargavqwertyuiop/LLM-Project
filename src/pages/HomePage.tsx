import React from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Paper,
} from '@mui/material';
import { Link } from 'react-router-dom';
import {
  Psychology,
  Analytics,
  Compare,
  CloudUpload,
  AutoAwesome,
  Speed,
} from '@mui/icons-material';

const HomePage: React.FC = () => {
  const features = [
    {
      icon: <CloudUpload sx={{ fontSize: 48, color: 'primary.main' }} />,
      title: 'Multi-Format Support',
      description: 'Upload and analyze PDF, DOCX, TXT, PPTX, XLSX, and CSV files',
      chips: ['PDF', 'DOCX', 'TXT', 'PPTX', 'XLSX', 'CSV'],
    },
    {
      icon: <AutoAwesome sx={{ fontSize: 48, color: 'secondary.main' }} />,
      title: 'AI-Powered Analysis',
      description: 'Multiple open-source LLMs for comprehensive text analysis',
      chips: ['Ollama', 'Hugging Face', 'Transformers'],
    },
    {
      icon: <Speed sx={{ fontSize: 48, color: 'success.main' }} />,
      title: 'Real-time Processing',
      description: 'Fast document processing and instant AI insights',
      chips: ['Real-time', 'Async', 'Scalable'],
    },
  ];

  const analysisTypes = [
    {
      icon: <Psychology />,
      title: 'Text Summarization',
      description: 'Generate concise summaries using multiple LLM models',
      path: '/analysis',
    },
    {
      icon: <Analytics />,
      title: 'Sentiment Analysis',
      description: 'Analyze emotional tone and sentiment in documents',
      path: '/analysis',
    },
    {
      icon: <Compare />,
      title: 'Document Comparison',
      description: 'Compare multiple documents for similarities and differences',
      path: '/compare',
    },
  ];

  return (
    <Container maxWidth="xl">
      {/* Hero Section */}
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h1" component="h1" gutterBottom>
          DocuMind
        </Typography>
        <Typography variant="h4" component="h2" color="text.secondary" gutterBottom>
          AI-Powered Document Analysis
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}>
          Harness the power of multiple open-source LLMs to analyze, summarize, and understand your documents
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button
            variant="contained"
            size="large"
            component={Link}
            to="/analysis"
            startIcon={<Analytics />}
            sx={{ px: 4, py: 1.5 }}
          >
            Start Analysis
          </Button>
          <Button
            variant="outlined"
            size="large"
            component={Link}
            to="/compare"
            startIcon={<Compare />}
            sx={{ px: 4, py: 1.5 }}
          >
            Compare Documents
          </Button>
        </Box>
      </Box>

      {/* Features Section */}
      <Box sx={{ py: 6 }}>
        <Typography variant="h2" component="h2" textAlign="center" gutterBottom>
          Key Features
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Paper
                elevation={3}
                sx={{
                  p: 4,
                  textAlign: 'center',
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                  },
                }}
              >
                <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h5" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 2, flexGrow: 1 }}>
                  {feature.description}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', justifyContent: 'center' }}>
                  {feature.chips.map((chip) => (
                    <Chip key={chip} label={chip} variant="outlined" size="small" />
                  ))}
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Analysis Types Section */}
      <Box sx={{ py: 6 }}>
        <Typography variant="h2" component="h2" textAlign="center" gutterBottom>
          Analysis Capabilities
        </Typography>
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {analysisTypes.map((analysis, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-2px)',
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                  <Box sx={{ mb: 2, color: 'primary.main' }}>{analysis.icon}</Box>
                  <Typography variant="h6" component="h3" gutterBottom>
                    {analysis.title}
                  </Typography>
                  <Typography color="text.secondary">
                    {analysis.description}
                  </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                  <Button
                    component={Link}
                    to={analysis.path}
                    variant="outlined"
                    startIcon={analysis.icon}
                  >
                    Try Now
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Technology Stack Section */}
      <Box sx={{ py: 6 }}>
        <Paper sx={{ p: 4, textAlign: 'center', backgroundColor: 'grey.50' }}>
          <Typography variant="h4" component="h2" gutterBottom>
            Powered by Open Source AI
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 3 }}>
            Built with cutting-edge open-source technologies
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
            {[
              'Ollama (Llama2, Mistral)',
              'Hugging Face Transformers',
              'Sentence Transformers',
              'FastAPI',
              'React',
              'Material-UI',
            ].map((tech) => (
              <Chip
                key={tech}
                label={tech}
                variant="filled"
                color="primary"
                sx={{ fontSize: '0.9rem', py: 1 }}
              />
            ))}
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default HomePage;