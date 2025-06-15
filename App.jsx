import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { AlertCircle, CheckCircle, FileText, Zap, Users, Globe, Code, BookOpen, Sparkles, Download, Github, ExternalLink } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('generator')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState(null)
  const [validationResults, setValidationResults] = useState(null)
  const [formData, setFormData] = useState({
    topic: '',
    audience: 'intermediate',
    keywords: '',
    length: 'medium'
  })

  // Simulate API calls to the MCP server
  const generateBlogPost = async () => {
    setIsGenerating(true)
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    // Mock generated content
    const mockContent = {
      title: `The Complete Guide to ${formData.topic}: Best Practices for ${formData.audience.charAt(0).toUpperCase() + formData.audience.slice(1)} Developers`,
      introduction: `In today's rapidly evolving technology landscape, ${formData.topic} has emerged as a critical component for modern development. This comprehensive guide will explore the fundamental concepts, practical implementations, and best practices that will help you master ${formData.topic} and leverage its full potential in your projects.`,
      content: `# ${formData.topic}: A Comprehensive Guide\n\n## Introduction\n\nIn today's rapidly evolving technology landscape, ${formData.topic} has emerged as a critical component for modern development...\n\n## Core Concepts\n\nUnderstanding the fundamental principles of ${formData.topic} is essential for effective implementation...\n\n## Implementation Guide\n\nThis section provides step-by-step guidance for implementing ${formData.topic} in your projects...\n\n## Best Practices\n\nFollowing established best practices ensures reliable and maintainable ${formData.topic} implementations...\n\n## Conclusion\n\nThroughout this guide, we've explored the essential aspects of ${formData.topic}...`,
      wordCount: 1250,
      readingTime: 6,
      sections: 5,
      keywords: formData.keywords.split(',').map(k => k.trim()).filter(k => k),
      generatedAt: new Date().toISOString()
    }
    
    const mockValidation = {
      overallValid: true,
      summary: {
        totalErrors: 0,
        totalWarnings: 1
      },
      validations: {
        title: { valid: true, errors: [], warnings: [], length: mockContent.title.length },
        structure: { valid: true, errors: [], warnings: ['Consider adding more external links'], mainSections: 5 }
      }
    }
    
    setGeneratedContent(mockContent)
    setValidationResults(mockValidation)
    setIsGenerating(false)
  }

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm dark:bg-slate-900/80 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              className="flex items-center space-x-3"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  MCP Technical Blog Server
                </h1>
                <p className="text-sm text-muted-foreground">AI-Powered Technical Content Generation</p>
              </div>
            </motion.div>
            
            <motion.div 
              className="flex items-center space-x-2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <Button variant="outline" size="sm" className="hidden sm:flex">
                <Github className="w-4 h-4 mr-2" />
                GitHub
              </Button>
              <Button variant="outline" size="sm" className="hidden sm:flex">
                <FileText className="w-4 h-4 mr-2" />
                Docs
              </Button>
            </motion.div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-16 px-4">
        <div className="container mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Generate Technical Blogs
              <br />
              <span className="text-3xl md:text-5xl">with AI Precision</span>
            </h2>
            <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
              Create high-quality technical blog posts with comprehensive business rules validation, 
              SEO optimization, and multi-audience support powered by the Model Context Protocol.
            </p>
          </motion.div>

          {/* Feature Cards */}
          <motion.div 
            className="grid md:grid-cols-3 gap-6 mb-12"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <Card className="border-0 shadow-lg bg-white/60 backdrop-blur-sm hover:shadow-xl transition-all duration-300">
              <CardHeader>
                <Zap className="w-8 h-8 text-blue-600 mb-2" />
                <CardTitle>Lightning Fast</CardTitle>
                <CardDescription>Generate complete blog posts in under 5 seconds with intelligent content creation</CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="border-0 shadow-lg bg-white/60 backdrop-blur-sm hover:shadow-xl transition-all duration-300">
              <CardHeader>
                <Users className="w-8 h-8 text-purple-600 mb-2" />
                <CardTitle>Multi-Audience</CardTitle>
                <CardDescription>Adapt content for beginner, intermediate, and advanced technical audiences</CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="border-0 shadow-lg bg-white/60 backdrop-blur-sm hover:shadow-xl transition-all duration-300">
              <CardHeader>
                <Globe className="w-8 h-8 text-indigo-600 mb-2" />
                <CardTitle>SEO Optimized</CardTitle>
                <CardDescription>Built-in SEO optimization with keyword integration and quality validation</CardDescription>
              </CardHeader>
            </Card>
          </motion.div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-8 px-4">
        <div className="container mx-auto max-w-6xl">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-8">
              <TabsTrigger value="generator" className="flex items-center space-x-2">
                <Sparkles className="w-4 h-4" />
                <span>Blog Generator</span>
              </TabsTrigger>
              <TabsTrigger value="validation" className="flex items-center space-x-2">
                <CheckCircle className="w-4 h-4" />
                <span>Validation</span>
              </TabsTrigger>
              <TabsTrigger value="api" className="flex items-center space-x-2">
                <Code className="w-4 h-4" />
                <span>API Reference</span>
              </TabsTrigger>
            </TabsList>

            {/* Blog Generator Tab */}
            <TabsContent value="generator" className="space-y-6">
              <div className="grid lg:grid-cols-2 gap-8">
                {/* Input Form */}
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <FileText className="w-5 h-5" />
                        <span>Blog Configuration</span>
                      </CardTitle>
                      <CardDescription>
                        Configure your technical blog post parameters
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="topic">Topic</Label>
                        <Input
                          id="topic"
                          placeholder="e.g., Docker Containerization, React Hooks, API Design"
                          value={formData.topic}
                          onChange={(e) => handleInputChange('topic', e.target.value)}
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="audience">Target Audience</Label>
                        <Select value={formData.audience} onValueChange={(value) => handleInputChange('audience', value)}>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="beginner">Beginner</SelectItem>
                            <SelectItem value="intermediate">Intermediate</SelectItem>
                            <SelectItem value="advanced">Advanced</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="keywords">Keywords (comma-separated)</Label>
                        <Input
                          id="keywords"
                          placeholder="e.g., containers, microservices, deployment"
                          value={formData.keywords}
                          onChange={(e) => handleInputChange('keywords', e.target.value)}
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="length">Content Length</Label>
                        <Select value={formData.length} onValueChange={(value) => handleInputChange('length', value)}>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="short">Short (800-1200 words)</SelectItem>
                            <SelectItem value="medium">Medium (1200-2000 words)</SelectItem>
                            <SelectItem value="long">Long (2000+ words)</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <Button 
                        onClick={generateBlogPost} 
                        disabled={!formData.topic || isGenerating}
                        className="w-full"
                        size="lg"
                      >
                        {isGenerating ? (
                          <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                            className="w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"
                          />
                        ) : (
                          <Sparkles className="w-4 h-4 mr-2" />
                        )}
                        {isGenerating ? 'Generating...' : 'Generate Blog Post'}
                      </Button>
                    </CardContent>
                  </Card>
                </motion.div>

                {/* Generated Content */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                >
                  <Card className="shadow-lg h-full">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <BookOpen className="w-5 h-5" />
                        <span>Generated Content</span>
                      </CardTitle>
                      <CardDescription>
                        Your AI-generated technical blog post
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <AnimatePresence mode="wait">
                        {isGenerating ? (
                          <motion.div
                            key="loading"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="flex flex-col items-center justify-center py-12 space-y-4"
                          >
                            <motion.div
                              animate={{ rotate: 360 }}
                              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                              className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full"
                            />
                            <p className="text-muted-foreground">Generating your blog post...</p>
                          </motion.div>
                        ) : generatedContent ? (
                          <motion.div
                            key="content"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="space-y-4"
                          >
                            <div className="flex flex-wrap gap-2 mb-4">
                              <Badge variant="secondary">{generatedContent.wordCount} words</Badge>
                              <Badge variant="secondary">{generatedContent.readingTime} min read</Badge>
                              <Badge variant="secondary">{generatedContent.sections} sections</Badge>
                              {validationResults?.overallValid && (
                                <Badge variant="default" className="bg-green-100 text-green-800">
                                  <CheckCircle className="w-3 h-3 mr-1" />
                                  Validated
                                </Badge>
                              )}
                            </div>
                            
                            <div className="space-y-3">
                              <div>
                                <Label className="text-sm font-medium">Title</Label>
                                <p className="text-lg font-semibold">{generatedContent.title}</p>
                              </div>
                              
                              <div>
                                <Label className="text-sm font-medium">Introduction</Label>
                                <p className="text-sm text-muted-foreground">{generatedContent.introduction}</p>
                              </div>
                              
                              <div className="flex space-x-2">
                                <Button size="sm" variant="outline">
                                  <Download className="w-4 h-4 mr-2" />
                                  Download
                                </Button>
                                <Button size="sm" variant="outline">
                                  <ExternalLink className="w-4 h-4 mr-2" />
                                  Preview
                                </Button>
                              </div>
                            </div>
                          </motion.div>
                        ) : (
                          <motion.div
                            key="empty"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex flex-col items-center justify-center py-12 text-center space-y-4"
                          >
                            <FileText className="w-16 h-16 text-muted-foreground/50" />
                            <div>
                              <p className="text-lg font-medium">No content generated yet</p>
                              <p className="text-sm text-muted-foreground">Fill in the form and click generate to create your blog post</p>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </CardContent>
                  </Card>
                </motion.div>
              </div>
            </TabsContent>

            {/* Validation Tab */}
            <TabsContent value="validation" className="space-y-6">
              <Card className="shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <CheckCircle className="w-5 h-5" />
                    <span>Business Rules Validation</span>
                  </CardTitle>
                  <CardDescription>
                    Comprehensive quality assurance for technical content
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {validationResults ? (
                    <div className="space-y-4">
                      <div className="flex items-center space-x-2">
                        {validationResults.overallValid ? (
                          <CheckCircle className="w-5 h-5 text-green-600" />
                        ) : (
                          <AlertCircle className="w-5 h-5 text-red-600" />
                        )}
                        <span className="font-medium">
                          {validationResults.overallValid ? 'All validations passed' : 'Validation issues found'}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div className="text-center p-4 bg-red-50 rounded-lg">
                          <div className="text-2xl font-bold text-red-600">{validationResults.summary.totalErrors}</div>
                          <div className="text-sm text-red-600">Errors</div>
                        </div>
                        <div className="text-center p-4 bg-yellow-50 rounded-lg">
                          <div className="text-2xl font-bold text-yellow-600">{validationResults.summary.totalWarnings}</div>
                          <div className="text-sm text-yellow-600">Warnings</div>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      Generate a blog post to see validation results
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            {/* API Reference Tab */}
            <TabsContent value="api" className="space-y-6">
              <Card className="shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Code className="w-5 h-5" />
                    <span>MCP API Reference</span>
                  </CardTitle>
                  <CardDescription>
                    Available tools and their parameters
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div className="border rounded-lg p-4">
                      <h4 className="font-semibold mb-2">generate_complete_blog</h4>
                      <p className="text-sm text-muted-foreground mb-3">Generate a complete technical blog post with full content</p>
                      <div className="bg-slate-100 dark:bg-slate-800 rounded p-3 text-sm font-mono">
                        {`{
  "topic": "string",
  "target_audience": "beginner|intermediate|advanced",
  "keywords": ["string"],
  "desired_length": "short|medium|long"
}`}
                      </div>
                    </div>
                    
                    <div className="border rounded-lg p-4">
                      <h4 className="font-semibold mb-2">validate_blog_post</h4>
                      <p className="text-sm text-muted-foreground mb-3">Validate content against business rules</p>
                      <div className="bg-slate-100 dark:bg-slate-800 rounded p-3 text-sm font-mono">
                        {`{
  "blog_post": {
    "title": "string",
    "content": "string",
    "introduction": "string",
    "conclusion": "string"
  }
}`}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white/80 backdrop-blur-sm dark:bg-slate-900/80 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-muted-foreground">
            <p>© 2025 MCP Technical Blog Server. Powered by Model Context Protocol.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

