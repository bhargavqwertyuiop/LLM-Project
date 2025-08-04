import React, { useState } from 'react';
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
  CircularProgress,
  Alert,
  Chip,
  IconButton,
  Divider,
} from '@mui/material';
import {
  Compare,
  Add,
  Delete,
  Analytics,
} from '@mui/icons-material';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

interface ComparisonResult {
  similarity_matrix?: number[][];
  average_similarity?: number;
  comparative_analysis?: string;
}

interface TextInfo {
  index: number;
  word_count: number;
  char_count: number;
}

const ComparePage: React.FC = () => {
  const [texts, setTexts] = useState<string[]>(['', '']);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<ComparisonResult | null>(null);
  const [textsInfo, setTextsInfo] = useState<TextInfo[]>([]);
  const [error, setError] = useState<string | null>(null);

  const addTextInput = () => {
    if (texts.length < 5) {
      setTexts([...texts, '']);
    }
  };

  const removeTextInput = (index: number) => {
    if (texts.length > 2) {
      const newTexts = texts.filter((_, i) => i !== index);
      setTexts(newTexts);
    }
  };

  const updateText = (index: number, value: string) => {
    const newTexts = [...texts];
    newTexts[index] = value;
    setTexts(newTexts);
  };

  const handleCompare = async () => {
    const nonEmptyTexts = texts.filter(text => text.trim());
    
    if (nonEmptyTexts.length < 2) {
      setError('Please enter at least 2 texts to compare');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);
    setTextsInfo([]);

    try {
      const response = await axios.post('/api/v1/compare-texts', {
        texts: nonEmptyTexts,
        comparison_aspects: ['similarity', 'key_differences'],
      });

      setResults(response.data.comparison_results);
      setTextsInfo(response.data.texts_info);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to compare texts');
    } finally {
      setLoading(false);
    }
  };

  const getSimilarityColor = (similarity: number) => {
    if (similarity > 0.8) return 'success';
    if (similarity > 0.5) return 'warning';
    return 'error';
  };

  const renderSimilarityMatrix = (matrix: number[][]) => {
    return (
      <Box sx={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Text</th>
              {matrix.map((_, index) => (
                <th key={index} style={{ padding: '8px', border: '1px solid #ddd' }}>
                  {index + 1}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, rowIndex) => (
              <tr key={rowIndex}>
                <td style={{ padding: '8px', border: '1px solid #ddd', fontWeight: 'bold' }}>
                  {rowIndex + 1}
                </td>
                {row.map((cell, colIndex) => (
                  <td
                    key={colIndex}
                    style={{
                      padding: '8px',
                      border: '1px solid #ddd',
                      textAlign: 'center',
                      backgroundColor: rowIndex === colIndex ? '#f5f5f5' : 'transparent',
                    }}
                  >
                    <Chip
                      label={cell.toFixed(3)}
                      color={rowIndex === colIndex ? 'default' : getSimilarityColor(cell)}
                      variant={rowIndex === colIndex ? 'outlined' : 'filled'}
                      size="small"
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </Box>
    );
  };

  return (
    <Container maxWidth="xl">
      <Typography variant="h2" component="h1" gutterBottom textAlign="center">
        Document Comparison
      </Typography>
      <Typography variant="h6" color="text.secondary" textAlign="center" sx={{ mb: 4 }}>
        Compare multiple texts to find similarities and differences
      </Typography>

      <Grid container spacing={4}>
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Texts to Compare
            </Typography>

            {texts.map((text, index) => (
              <Box key={index} sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Text {index + 1}
                  </Typography>
                  {texts.length > 2 && (
                    <IconButton
                      onClick={() => removeTextInput(index)}
                      color="error"
                      size="small"
                    >
                      <Delete />
                    </IconButton>
                  )}
                </Box>
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  placeholder={`Enter text ${index + 1} here...`}
                  value={text}
                  onChange={(e) => updateText(index, e.target.value)}
                  variant="outlined"
                />
                <Typography variant="caption" color="text.secondary">
                  Words: {text.split(/\s+/).filter(word => word.length > 0).length} | 
                  Characters: {text.length}
                </Typography>
              </Box>
            ))}

            {texts.length < 5 && (
              <Button
                variant="outlined"
                startIcon={<Add />}
                onClick={addTextInput}
                sx={{ mb: 3 }}
              >
                Add Another Text
              </Button>
            )}

            <Divider sx={{ my: 3 }} />

                         <Button
               variant="contained"
               size="medium"
               startIcon={loading ? <CircularProgress size={20} /> : <Compare />}
               onClick={handleCompare}
               disabled={loading || texts.filter(t => t.trim()).length < 2}
               fullWidth
               sx={{ py: 1.5, fontSize: '1.1rem' }}
             >
              {loading ? 'Comparing...' : 'Compare Texts'}
            </Button>
          </Paper>
        </Grid>

        {/* Results Section */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, minHeight: 400 }}>
            <Typography variant="h5" gutterBottom>
              Comparison Results
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

            {results && (
              <Box>
                {/* Text Information */}
                {textsInfo.length > 0 && (
                  <Card sx={{ mb: 3, backgroundColor: 'info.50' }}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Text Statistics
                      </Typography>
                      <Grid container spacing={2}>
                        {textsInfo.map((info) => (
                          <Grid item xs={12} sm={6} key={info.index}>
                            <Typography variant="body2">
                              <strong>Text {info.index + 1}:</strong> {info.word_count} words, {info.char_count} characters
                            </Typography>
                          </Grid>
                        ))}
                      </Grid>
                    </CardContent>
                  </Card>
                )}

                {/* Similarity Analysis */}
                {results.similarity_matrix && (
                  <Card sx={{ mb: 3 }}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Similarity Matrix
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Values range from 0 (completely different) to 1 (identical)
                      </Typography>
                      {renderSimilarityMatrix(results.similarity_matrix)}
                      
                      {results.average_similarity !== undefined && (
                        <Box sx={{ mt: 2, textAlign: 'center' }}>
                          <Chip
                            label={`Average Similarity: ${(results.average_similarity * 100).toFixed(1)}%`}
                            color={getSimilarityColor(results.average_similarity)}
                            variant="filled"
                            sx={{ fontSize: '1rem', py: 1, px: 2 }}
                          />
                        </Box>
                      )}
                    </CardContent>
                  </Card>
                )}

                {/* Comparative Analysis */}
                {results.comparative_analysis && (
                  <Card sx={{ mb: 3 }}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        AI Analysis
                      </Typography>
                      <Paper sx={{ p: 2, backgroundColor: 'grey.50' }}>
                        <ReactMarkdown>{results.comparative_analysis}</ReactMarkdown>
                      </Paper>
                    </CardContent>
                  </Card>
                )}
              </Box>
            )}

            {!loading && !results && !error && (
              <Box sx={{ textAlign: 'center', py: 4, color: 'text.secondary' }}>
                <Compare sx={{ fontSize: 64, mb: 2 }} />
                <Typography variant="h6">
                  Enter at least 2 texts to see comparison results
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  The AI will analyze similarities, differences, and provide insights
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Instructions */}
      <Paper sx={{ p: 3, mt: 4, backgroundColor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom>
          How It Works
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Analytics sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Semantic Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Uses sentence transformers to generate embeddings and calculate semantic similarity
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Compare sx={{ fontSize: 48, color: 'secondary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                AI Comparison
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Leverages open-source LLMs to identify key similarities and differences
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography sx={{ fontSize: 48, mb: 1 }}>📊</Typography>
              <Typography variant="h6" gutterBottom>
                Visual Results
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Interactive similarity matrix and detailed analysis reports
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default ComparePage;