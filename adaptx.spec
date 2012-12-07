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
rm -rf $RPM_BUILD_ROOT

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}_%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})
rm -rf build/doc/javadoc

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.13-4.1.8mdv2011.0
+ Revision: 662753
- mass rebuild

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.13-4.1.7mdv2011.0
+ Revision: 603171
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.13-4.1.6mdv2010.1
+ Revision: 521933
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.13-4.1.5mdv2010.0
+ Revision: 413023
- rebuild

* Thu Dec 20 2007 Olivier Blin <oblin@mandriva.com> 0.9.13-4.1.4mdv2009.0
+ Revision: 135817
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0.9.13-4.1.4mdv2008.1
+ Revision: 120822
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0.9.13-4.1.3mdv2008.0
+ Revision: 87186
- rebuild to filter out autorequires on GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Jul 18 2007 Anssi Hannula <anssi@mandriva.org> 0.9.13-4.1.2mdv2008.0
+ Revision: 53180
- use xml-commons-jaxp-1.3-apis explicitely instead of the generic
  xml-commons-apis which is provided by multiple packages (see bug #31473)

* Wed Jul 04 2007 David Walluck <walluck@mandriva.org> 0.9.13-4.1.1mdv2008.0
+ Revision: 48209
- sync with FC7
- fix javadoc build

  + Anssi Hannula <anssi@mandriva.org>
    - rebuild with new libgcj


* Tue Oct 31 2006 David Walluck <walluck@mandriva.org> 0.9.13-3.3mdv2007.0
+ Revision: 73971
- add log4j to build classpath
- BuildRequires: log4j
- 0.9.13
- Import adaptx

* Thu Aug 10 2006 David Walluck <walluck@mandriva.org> 0:0.9.6-3.1mdv2007.0
- fix Requires

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0.9.6-2.6mdv2007.0
- rebuild for libgcj.so.7
- own %%{_libdir}/gcj/%%{name}

* Tue Jan 17 2006 David Walluck <walluck@mandriva.org> 0:0.9.6-2.5mdk
- fix CLASSPATH when building docs

* Sun Jan 15 2006 David Walluck <walluck@mandriva.org> 0:0.9.6-2.4mdk
- BuildRequires: java-devel
- enable the debug package
- set OPT_JAR_LIST for doc even though it seems to build without it

* Wed Jan 11 2006 David Walluck <walluck@mandriva.org> 0:0.9.6-2.3mdk
- (Build)Requires: xerces-j2
- export OPT_JAR_LIST=
- change License

* Fri Dec 02 2005 David Walluck <walluck@mandriva.org> 0:0.9.6-2.2mdk
- add post scripts

* Fri Dec 02 2005 David Walluck <walluck@mandriva.org> 0:0.9.6-2.1mdk
- sync with 0:0.9.6-2jpp
- aot-compile

* Sun Sep 11 2005 David Walluck <walluck@mandriva.org> 0:0.9.6-1.1mdk
- release

* Fri Jun 17 2005 Gary Benson <gbenson@redhat.com> 0:0.9.6-1jpp_1fc
- Build into Fedora.

* Fri Jun 10 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles from the tarball.

* Thu Jun 02 2005 Gary Benson <gbenson@redhat.com>
- Remove all jarfiles before building.

* Fri Mar 05 2004 Frank Ch. Eigler <fche@redhat.com> 0:0.9.6-1jpp_1rh
- RH vacuuming
- build with internal adaptx for the moment

