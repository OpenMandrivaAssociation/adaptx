# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

Name:          adaptx
Version:       0.9.13
Release:       %mkrel 4.1.8
Summary:       AdaptX XSLT processor and XPath engine
License:       BSD
Group:         Development/Java
# svn export http://svn.codehaus.org/castor/adaptx/tags/0.9.13/ adaptx-0.9.13-src
# tar cjf adaptx-0.9.13-src.tar.bz2 adaptx-0.9.13-src
Source0:       %{name}-%{version}-src.tar.bz2

Patch0:        %{name}-%{version}-xsl.patch
Patch1:        %{name}-%{version}-missingstubs.patch
Url:           http://castor.codehaus.org/
BuildRequires: ant >= 0:1.6
BuildRequires: java-rpmbuild >= 0:1.6
BuildRequires: log4j
BuildRequires: xml-commons-jaxp-1.3-apis
BuildRequires: xerces-j2
Requires:      log4j
Requires:      xml-commons-jaxp-1.3-apis
Requires:      xerces-j2
Requires(pre):    jpackage-utils
Requires(postun): jpackage-utils
%if ! %{gcj_support}
BuildArch:    noarch
%endif
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%description
Adaptx is an XSLT processor and XPath engine.

%package javadoc
Group:            Development/Java
Summary:          Javadoc for %{name}
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description javadoc
Javadoc for %{name}.

%package doc
Summary:    Documentation for %{name}
Group:      Development/Java

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}-src
# remove CVS internal files
for dir in `find . -type d -name CVS`; do rm -rf $dir; done
# remove all binary libs
for j in $(find . -name "*.jar"); do
    %{__rm} $j
done

%patch0
%patch1

# (walluck): fix javadoc parsing
for file in `%{__grep} -rl 'enum[\\. ]' *`; do
    %{__perl} -pi -e 's/enum/en/g' $file
done

%build
perl -p -i -e 's|classic|modern|' src/build.xml
export CLASSPATH=$(build-classpath xml-commons-jaxp-1.3-apis log4j xerces-j2)
%{ant} -buildfile src/build.xml jar javadoc
CLASSPATH=$CLASSPATH:dist/adaptx_%{version}.jar
%{ant} -buildfile src/build.xml doc

%install
rm -rf %{buildroot}

# jar
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/%{name}_%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/doc/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})
rm -rf build/doc/javadoc

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0664,root,root,0755)
%doc src/etc/{CHANGELOG,contributors.html,LICENSE}
%{_javadir}/*

%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0664,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%dir %{_javadocdir}/%{name}

%files doc
%defattr(0664,root,root,0755)
%doc build/doc/*
